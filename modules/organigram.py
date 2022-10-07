from flask import Flask, redirect, request,jsonify, Blueprint, json
import pymongo
ORGANIGRAM_REQ = Blueprint('organigram', __name__)
