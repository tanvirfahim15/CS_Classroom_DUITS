from classes.management_class.ObserverPattern.IEnrollmentObserver import IEnrollmentObserver
from flask import Blueprint
from bson import ObjectId
from flask import Flask, render_template, request, redirect, session
from Database.database import db

class AdminObserver(IEnrollmentObserver):

    def __init__(self):
        pass


    def update(self, studentEnroll, techerEnroll):
        print('here printing admin update')
        print(studentEnroll)
        print(techerEnroll)


        if studentEnroll:
            enroll_stu = db.xenrolled_student
            enroll_stu.insert_one(studentEnroll)

        if techerEnroll:
            enroll_tech=db.xenrolled_techer
            enroll_tech.insert_one(techerEnroll)

        return

