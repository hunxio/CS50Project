import os
import sqlite3
import argon2
import requests
from flask import Flask, render_template, redirect, request, session


# It will close the database connection and return an error page #
def ErrorConnection(con, code_error):
    con.close()
    return render_template("errorpage.html", message=code_error)


# Basic template for error page, in case no access to the database and user did not login #
def ErrorTemplate(code_error):
    return render_template("errorpage.html", message=code_error)


# Access to database and looks for user's username by filtering by email (session host)
def acquireSessionEmail(cur):
    email = session.get("email")
    usernameCur = cur.execute("SELECT username FROM users WHERE email = ?;", (email,))
    userUsername = usernameCur.fetchone()[0]
    return userUsername


def hashPassword(password):
    # Password hash and salt with argon2 #
    hasher = argon2.PasswordHasher()
    hashPassword = hasher.hash(password)
    return hashPassword
    
# API SERVICE PROVIDED BY https://www.themoviedb.org/ #
def movieapi(movie_id):

    url = " https://api.themoviedb.org/3/movie/" + str(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZDFiZWY5ZDNhMmM2YjljOWZiMGJhNzBmMGM4MmEyMyIsInN1YiI6IjY2MmJhNTRiNmYzMWFmMDExZmI3NTIwMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YSjZO6oBSn3tqJLP5l6KLG12wzod-xZEiYVzxxOfpwQ"
    }

    response = requests.get(url, headers=headers)
    original_title = response.json()["original_title"]
    return original_title

