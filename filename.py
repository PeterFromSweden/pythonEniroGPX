import re
import string


def make_valid(input_string):
    """
    Converts an input string into a valid filename.
    Removes characters that aren't allowed in filenames.
    Retains only letters, digits, underscores, hyphens, and dots.
    """
    # Make the filename lowercase?
    # filename = input_string.lower()
    filename = input_string

    # Remove characters that are not allowed in filenames
    allowed_chars = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + " -_.åäöÅÄÖ")
    cleaned_filename = "".join(c if c in allowed_chars else "_" for c in filename)

    # Strip leading and trailing hyphens
    cleaned_filename = cleaned_filename.strip("-")

    return cleaned_filename


if __name__ == '__main__':
    # Example usage:
    input_string = "Nyköping - Ålö File: Name (with Special Characters)"
    valid_filename = make_valid(input_string)
    print(f"Original string: {input_string}")
    print(f"Valid filename: {valid_filename}")
