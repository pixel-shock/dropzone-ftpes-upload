# Dropzone Action Info
# Name: FTPES Upload
# Description: Provides an action to upload your files to a FTPES Server
# Handles: Files
# Creator: Tino Wehe
# URL: https://github.com/pixel-shock/dropzone-ftpes-upload.git
# Events: Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.5
# OptionsNIB: ExtendedLogin
# UniqueID: e0b4a398-b280-46c3-afe7-f45d8291b018

import ftplib
import os
import socket

from com.brandrockers.ftpes.ftpes import FTPES
from com.brandrockers.zip.zip import ZIP


def handle_upload_state(progress, ftpes_instance, do_update):
    # this is due the animation delay time of the menubar icon,
    # so it should not trigger the process event too often
    """
    Handle the upload progress of the FTPES class.

    @param progress: The current upload progress in percent.
    @type progress: Integer
    @param ftpes_instance: An instance of the FTPES class.
    @type ftpes_instance: Object
    @param do_update: A boolean that determines if the upload handler should update the progress state of dropzone.
    @type do_update: Boolean
    """
    if do_update is True:
        dz.percent(progress)

    if progress >= 100:
        tmp_root_path = ''

        if os.environ.get('root_url') is not None:
            tmp_root_path = os.environ.get('root_url')

        upload_path = os.path.join(tmp_root_path, ftpes_instance.upload_path)
        dz.finish('FTPES upload for "%s" done!' % upload_path)
        dz.url(upload_path)


def dragged():
    """
    The handler which will be called from dropzone if the user drags files onto the icon.
    """
    #
    # Save all dropzone vars
    #
    host = os.environ.get('server')
    port = os.environ.get('port')
    username = os.environ.get('username')
    password = os.environ.get('password')
    remote_path = os.environ.get('remote_path')
    output_name = dz.inputbox("Please enter the filename for the zip file!", "Filename:").replace('.zip', '') + '.zip'
    tmp_directory = dz.temp_folder()

    if host is None:
        dz.error("Error", "You must specify a hostname!")

    try:
        dz.begin('Running FTPES Task for "%s"!' % output_name)  # set begin state for dropzone
        dz.determinate(False)  # set determinate to false, because the zipping process has no progress
        zipper = ZIP(items, tmp_directory, output_name)  # create a new ZIP instance
        zipper.zip()  # try to zip all files
        ftpes = FTPES(host, port, username, password, remote_path,
                      zipper.absolute_zipfile_path)  # create a new FTPES instance
        try:
            ftpes.connect()  # try to connect to the FTP server
            try:
                ftpes.login()  # Try to login to the FTP server
                try:
                    ftpes.cwd()  # Try to change the working directory
                    dz.determinate(True)  # set determinate to True to set progress updates for dropzone
                    ftpes.upload(handle_upload_state)  # Try to upload the zip file
                    zipper.cleanup()  # Delete the zip file from dropzones tmp directory
                except ftplib.error_perm, msg:
                    zipper.cleanup()  # Delete the zip file from dropzones tmp directory
                    dz.error("Error", msg)  # throw the error to dropzone
            except ftplib.error_perm, msg:
                zipper.cleanup()  # Delete the zip file from dropzones tmp directory
                dz.error("Error", msg)  # throw the error to dropzone
        except socket.gaierror, msg:
            zipper.cleanup()  # Delete the zip file from dropzones tmp directory
            dz.error("Error", msg)  # throw the error to dropzone
    except OSError as exception:
        dz.error("Error", exception.strerror)  # throw the error to dropzone
