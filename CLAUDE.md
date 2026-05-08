# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

### Role
You are a senior software engineer with more than 10 years of experience in software development. You are an expert in developing web applications running on mobile devices. As an expert in this field, you are aware of the existence of various technologies and tools that can be used to develop web applications running on mobile devices. You are also aware of the latest trends and best practices in this field.

### Background
I am working on a project that requires building a web application for a company that sells water measurement gauges. The used gauges are mechanical and they are not connected to the internet. The technician will visit the customer site and record the water measurement data by taking photos of the gauges.

## Project
Greenfield web application for a water-utility company. This project should run on a VPS server in the internet. It should be accessible by a technician via a mobile phone and a manager via a desktop computer. The app should be responsive and work on different screen sizes. The app should be accessible via a web browser. The app should be secure and the user credentials should be stored encrypted in the database. 

Create a database based on a Django model. In the database there are customers, sites, groups of sites, water gauges with serial numbers and other data. Each site can have multiple gauges. Each customer can have multiple sites. Each group can have multiple sites. Gauges belong to the site.
The database model and the maintenance is done via a django backend. This is just for the frontend for the technician and the manager. The manager will use the app to see the data and the technician will use the app to record the data.

The technician visits customer sites and photograph mechanical (non-networked) water meters. The app extracts the **serial number** and **consumed volume** from each photo via OCR, lets the technician verify and correct the result, and stores it. Managers later review and annotate the readings.

The database and administration is done via a Django backend. If possible also the frontend should be created using Django templates.

UI is **German only**.


### Task 1 - Backend
1. create a django project
2. create a django app for the technician
3. create a django app for the manager
4. create a django app for the admin
5. create database tables for:
- customer
- site
- group of sites
- water gauge
- technician
- manager
- admin
- reading
- photo



### Task 2 - Frontend
The service technician uses the web app on the mobile phone which is connected to the internet. The app should have the following features:

1. Take a photo of the gauge
2. Let the technician select the photo from the photo gallery
3. The technician can review the image before it gets uploaded
4. Upload the photo to the server
5. The photo is stored on the server
6. The technician can view the photo on the server
7. The serial number on the gauge is automatically extracted from the photo using OCR
8. The consumed volume is also shown on the photo and should be extracted using OCR
9. The technician should be able to verify the extracted data and correct it if necessary
10. The image, serial number and consumed volume are stored on the server

### Task 3
The manager uses the web app on the desktop computer which is connected to the internet. The app should have the following features:

1. The manager can view the photo on the server
2. The manager can view the serial number on the server
3. The manager can view the consumed volume on the server
4. The manager can add notes to the photo
5. The manager can add notes to the serial number
6. The manager can add notes to the gauge
7. The manager can add notes to the customer site

### Task 4
1. The manager can create different user accounts
2. all password user credentials are stored encrypted in the database
3. The manager can assign technician users to sites
4. The manager can assign specific gauges to technicians
5. the technician will only see the gauges that are assigned to him

### Task 5
Different Persons are organized in a database which can be modified by the manager. Persons can be:
- customer
- technician
- manager
- admin

Each Person is identified with a unique id. the existing gauges table belongs to a customer and must be moved to the customer table. Each customer has many gauges. The gauges table should contain:
- gauge_id: unique id
- serial_number: unique id
- consumed_volume: consumed volume
- location (latitude, longitude): location of the gauge
- additional_data (JSON): additional data about the gauge


customers have the following tables:
- Customer: Customer_ID, name, address, contactPerson, contactPersonPhone, contactPersonEmail, dateMemberSince
- ParentGroup: ParentGroup_ID, ParentGroup_Name
- array of Gauge objects: Gauge_ID, ParentGroup_ID, serial_number, consumed_volume, location (latitude, longitude), additional_data (JSON)
- User: User_ID, name, email, password


modify the existing webapplication to support the following features for customers, technicians and managers:
- import all customers and their gauges from a csv file.
- create manual entries for customers and their gauges.
- update entries
- delete entries
- search entries
- filter entries
- export all customers and their gauges to a csv file.
