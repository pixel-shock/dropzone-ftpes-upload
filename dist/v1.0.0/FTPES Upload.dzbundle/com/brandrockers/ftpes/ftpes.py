import ftplib
import math
import os
from ftplib import FTP_TLS, socket


class FTPES:
    def __init__(self, host, port=None, username=None, password=None, remote_path=None, absolute_zipfile_path=None):
        """
        This is a helper class to manage the FTP commands from the ftplib.

        @param host: The host for the connection.
        @type host: String
        @param port: The post for the connection.
        @type port: Integer
        @param username: The username for the connection. Leave blank to use "anonymous".
        @type username: String
        @param password: The password for the connection. Leave empty for none.
        @type password: String
        @param remote_path: The remote path of the server in which the zip file should be uploaded. If the path does not
                            exists, it will be created (recursive).
        @type remote_path: String
        @param absolute_zipfile_path: The absolute LOCAL filepath of the zip file.
        @type absolute_zipfile_path: String
        """
        self.ftps = None
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._remote_path = remote_path
        self._absolute_zipfile_path = absolute_zipfile_path
        self._bytesWritten = 0;
        self._totalFileSize = os.path.getsize(self._absolute_zipfile_path)
        self._uploadCallback = None
        self._currentProgress = 0

        # make the remote path relative if it isnt absolute or relative yet
        if self._remote_path is not None and self._remote_path.startswith(
                '.') is False and self._remote_path.startswith('/') is False:
            self._remote_path = './' + self._remote_path

        if self._username is None:
            self._username = 'anonymous'

        if self._port is None:
            self._port = 22

    def connect(self):
        """
        Try to connect to the FTP server.
        Raise an error if something went wrong.
        """
        try:
            self.ftps = FTP_TLS()
            self.ftps.set_pasv(True)
            self.ftps.connect(self._host, self._port)
        except socket.gaierror:
            raise

    def login(self):
        """
        Try to login in on the FTP server.
        Raise an error if something went wrong.
        """
        try:
            self.ftps.login(self._username, self._password)
            self.ftps.prot_p()
        except ftplib.error_perm:
            raise

    def cwd(self):
        """
        Try to switch the working directory on the FTP server (if set in the settings).
        If the path does not exist, it will be created.
        """
        if self._remote_path is not None:
            try:
                self.ftps.cwd(self._remote_path)
            except ftplib.error_perm:
                self.create_directory_tree(self._remote_path)
            except IOError:
                raise

    def create_directory_tree(self, current_directory):
        """
        Helper function to create the remote path.

        @param current_directory: The current working directory.
        @type current_directory: String
        """
        if current_directory is not "":
            try:
                self.ftps.cwd(current_directory)
            except ftplib.error_perm:
                self.create_directory_tree("/".join(current_directory.split("/")[:-1]))
                self.ftps.mkd(current_directory)
                self.ftps.cwd(current_directory)
            except IOError:
                raise

    def upload(self, callback=None):
        """
        The upload function.

        @param callback: The callback function for the upload progress.
        @type callback: Function
        """
        self._uploadCallback = callback
        zipfile_to_upload = open(self._absolute_zipfile_path, 'rb')
        zipfile_basename = os.path.basename(self._absolute_zipfile_path)
        self.ftps.storbinary('STOR %s' % zipfile_basename, zipfile_to_upload, 1024, self.handle_upload_state)
        zipfile_to_upload.close()

    def handle_upload_state(self, block):
        """
        The callback function for the upload progress.

        @param block: The StringIO of the current upload state
        @type block: StringIO
        """
        self._bytesWritten += 1024
        progress = math.floor((float(self._bytesWritten) / float(self._totalFileSize)) * 100)
        do_update = False

        if progress > self._currentProgress:
            do_update = True
            self._currentProgress = progress

        if self._uploadCallback is not None:
            self._uploadCallback(progress, self, do_update)

    def quit(self):
        """
        Try to quit everything and close the session.
        """
        self.ftps.quit()

    @property
    def upload_path(self):
        """
        Returns the upload path of the FTP server.

        @return: The path of the uploaded file on the FTP server.
        @rtype: String
        """
        tmp_remote_path = ''

        if self._remote_path is not None:
            tmp_remote_path = self._remote_path

        return os.path.join(tmp_remote_path, os.path.basename(self._absolute_zipfile_path))
