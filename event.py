from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn
@app.route('/event/')
def event():
    eID = request.args.get('eID')
    eName = request.args.get('eName')
    return render_template('event.html', eID=eID, eName=eName)