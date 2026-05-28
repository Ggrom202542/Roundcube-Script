# Mail Document System Architecture

## Overview

ระบบนี้ใช้สำหรับ:

* แปลง Raw Mail File เป็น EML
* อ่านข้อมูลอีเมล
* แตกไฟล์แนบ
* จัดเก็บข้อมูลเอกสาร
* รองรับระบบ Auto Processing ในอนาคต

---

# Architecture

GUI Layer
↓
Service Layer
↓
Core Engine
↓
Storage Layer

---

# Modules

## core/

ระบบประมวลผลหลัก

## services/

Business Logic

## gui/

User Interface

## docs/

Documentation

---

# Future Plan

* Attachment Extractor
* Database System
* Auto Scan Folder
* Update System
* Search System
* OCR
* PDF Preview
