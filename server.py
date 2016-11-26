# -*- coding: utf-8 -*-

from bottle import get, post, request, abort, run, static_file
from classifier import get_behaviours

hints = {
    'breakfast': '',
    'lunch': '',
    'dinner': '',
    'groceries': '',
    'snacks': '',
    'clothes': '',
    'electronics': '',
    'medication': '',
    'culture': '',
    'sports': '',
    'train': '',
    'travel': '',
    'gasoline': '',
    'bar': '',
    'loan': ''
}


@get('/')
def index():
    triggered_behaviours = get_behaviours('./datasimulation/tm.json')
    return hints[triggered_behaviours[0]]

run(host='localhost', port='8080')