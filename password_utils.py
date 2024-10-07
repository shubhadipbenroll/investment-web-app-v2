import base64
import binascii
import logging
import re

# Regular expression to check if the string looks like Base64
base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')

def decode_password(encoded_password):
    try:
        # Check if the password looks like a Base64-encoded string
        if not base64_pattern.match(encoded_password):
            logging.warning(f"Password does not appear to be Base64 encoded: {encoded_password}")
            return encoded_password  # Return the password as-is, it's likely plain text
        
        # Add padding if necessary
        missing_padding = len(encoded_password) % 4
        if missing_padding:
            encoded_password += '=' * (4 - missing_padding)
        
        # Decode Base64
        decoded_bytes = base64.b64decode(encoded_password)
        decoded_password = decoded_bytes.decode('utf-8')
        return decoded_password
    except (binascii.Error, ValueError, UnicodeDecodeError) as e:
        logging.error(f"Invalid Base64 string: {encoded_password} - Error: {e}")
        return None  # Return None for invalid passwords
