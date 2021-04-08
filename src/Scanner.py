import subprocess


def scan_image(outfile):
    """Gets an image from a connected scanning device and saves it
    as a TIF file at specified location.

    Throws a IOError if there is an error reading from the scanning device.

    Parameters:
        outfile (str): Path where scanned image should be saved.
    """
    try:
        cmd = 'scanimage --resolution 10 --mode Gray --format tiff > \'{outfile}.tif\''
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return f'{outfile}.tif'
    except:
        if error is None:
            error = 'Failed to scan image'

        raise IOError(error)
