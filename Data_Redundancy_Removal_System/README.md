# Data Redundancy Removal System

## Overview

The Data Redundancy Removal System is a Cloud Computing project developed to identify, validate, and prevent duplicate data from being stored in a database. The system uses SHA-256 hashing and SQLite database validation to ensure that only unique and verified data entries are stored.

## Objective

* Identify redundant data.
* Validate new data against existing records.
* Prevent duplicate data from entering the database.
* Store only unique and verified entries.
* Improve database efficiency and accuracy.

## Features

* SHA-256 based file validation
* Duplicate file detection
* SQLite database integration
* Upload history tracking
* Dashboard statistics
* Date and time logging
* Unique file storage
* Storage optimization

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* SHA-256 Hashing

## System Workflow

1. User uploads a file.
2. SHA-256 hash is generated.
3. Database checks for existing hash values.
4. Duplicate files are rejected.
5. Unique files are stored.
6. Upload history and statistics are updated.

## Project Structure

CodeAlpha_Data_Redundancy_Removal_System/

├── app.py

├── database.db

├── requirements.txt

├── cloud_storage/

└── README.md

## Output

* Unique File Stored Successfully
* Duplicate File Detected! Storage Prevented

## Benefits

* Reduces storage waste
* Improves database efficiency
* Prevents redundant data storage
* Maintains data integrity

## Author

Yaseera

CodeAlpha Cloud Computing Internship
