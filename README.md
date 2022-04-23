# Todo App

---

# Introduction

This is my first project with flask. It consists on a todo list app in which you have to register and can create, delete or change the status of todos. At the time this is written, this project is deployed at: https://flask-todolist-production-1.rj.r.appspot.com

# Database

It is thought to work with a **`gcloud firestore`** database. Before being able to run it, a gcloud project needs to be created and set as default using **`gcloud sdk`**.

# Secret key

A **`key`** at app/config.py has to be set. The default is ‘SUPER SECRET’ but it is not recommended at all to use ir.
