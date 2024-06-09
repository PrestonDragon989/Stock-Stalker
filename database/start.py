""" Database starter class file. """
import threading

import sys

import pymongo.errors

from tkinter import messagebox


class DatabaseStarter:
    """ An independent thread starter for the database, for seamless GUI opening. """
    def __init__(self) -> None:
        """ Constructor for DBS, contains private variable db. """
        self._database = None

    def database(self) -> object:
        """ Returns private variable db. """
        return self._database

    def capture(self) -> None:
        """ Tries to connect to the MongoDB database. If it does, captures the output and assigns it to self._db. Else,
        trigger a connection error message and exit. """
        try:
            import database.user as db
            self._database = db
        except (pymongo.errors.ConfigurationError, TypeError):
            messagebox.showinfo("Connection Error",
                                "STALKER could not connect. Make sure you have internet, and try again later.")
            sys.exit()

    def start(self) -> None:
        """ Starting the thread that independently runs the capture method. """
        start_db = threading.Thread(target=self.capture, daemon=True)
        start_db.start()
