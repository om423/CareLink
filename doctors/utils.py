"""Utility functions for doctors app."""

import math

import requests
from django.db.models import Q


def geocode_location(location_string, retries=3, delay=1):
    """
    Convert a location string to latitude and longitude coordinates.
    Uses OpenStreetMap Nominatim API (free, no API key required).

    Args:
        location_string (str): Location string like "Atlanta, GA" or full address
        retries (int): Number of retry attempts
        delay (float): Delay between retries in seconds

    Returns:
        tuple: (latitude, longitude) or (None, None) if geocoding fails
    """
    import time

    if not location_string or location_string.strip() == "":
        return None, None

    for attempt in range(retries):
        try:
            # Use OpenStreetMap Nominatim API (free)
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": location_string, "format": "json", "limit": 1, "addressdetails": 1}
            headers = {"User-Agent": "CareLink/1.0 (Telehealth Application)"}

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data and len(data) > 0:
                result = data[0]
                lat = float(result["lat"])
                lon = float(result["lon"])
                return lat, lon

            # If no results, return None
            return None, None

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 503:
                # Service unavailable, wait and retry
                if attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
                    continue
            print(f"Geocoding error for '{location_string}': {e}")
        except (requests.RequestException, ValueError, KeyError, IndexError) as e:
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
                continue
            print(f"Geocoding error for '{location_string}': {e}")

    return None, None


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth
    using the Haversine formula. Returns distance in miles.

    Args:
        lat1, lon1: First point coordinates (latitude, longitude)
        lat2, lon2: Second point coordinates (latitude, longitude)

    Returns:
        float: Distance in miles
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in miles
    r = 3959

    return c * r


def geocode_doctor_locations():
    """
    Geocode all doctor profiles that don't have coordinates yet.
    This is a utility function to populate existing doctors with coordinates.
    """
    from .models import DoctorProfile

    doctors_without_coords = DoctorProfile.objects.filter(
        clinic_latitude__isnull=True, clinic_longitude__isnull=True
    ).exclude(Q(clinic_address__isnull=True) | Q(clinic_address=""))

    geocoded_count = 0

    for doctor in doctors_without_coords:
        lat, lon = geocode_location(doctor.clinic_address)
        if lat is not None and lon is not None:
            doctor.clinic_latitude = lat
            doctor.clinic_longitude = lon
            doctor.save()
            geocoded_count += 1
            print(f"Geocoded: {doctor.clinic_name} at {doctor.clinic_address} -> ({lat}, {lon})")
        else:
            print(f"Failed to geocode: {doctor.clinic_name} at {doctor.clinic_address}")

    print(f"Successfully geocoded {geocoded_count} doctors")
    return geocoded_count
