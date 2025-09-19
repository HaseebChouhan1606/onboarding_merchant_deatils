# from flask import Flask, render_template_string, request, send_file, redirect, url_for, session
# from PyPDF2 import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# import io
# import re
# import requests
# import json

# app = Flask(__name__)
# app.secret_key = 'haseeb_key'  # Change this to a random secret key

# # Google Sheets configuration
# GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyN-kwS8MMUohF9-B_J0ANaohOAgWCGfZYJGzvVLLSoh0MipEmsNlQnA0MEcH-tN3nn/exec"  # Replace with your Google Apps Script web app URL

# # ---------------- SAFE TEXT HELPER ----------------
# def safe_text(value):
#     return str(value) if value else ""

# # ---------------- PDF GENERATION FUNCTION ----------------
# # Generate PDF in memory
# def generate_filled_pdf(texts, safe_name):
#     input_pdf_path = r"C:\Users\HP\Desktop\Projects\A4 Merchant Form.pdf"
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     # Group text per page
#     page_texts = {}
#     for text, x, y, page_number in texts:
#         page_texts.setdefault(page_number, []).append((text, x, y))

#     for page_num in range(len(reader.pages)):
#         page = reader.pages[page_num]

#         if page_num in page_texts:
#             packet = io.BytesIO()
#             c = canvas.Canvas(packet, pagesize=letter)
#             for text, x, y in page_texts[page_num]:
#                 c.drawString(x, y, safe_text(text))
#             c.save()

#             packet.seek(0)
#             new_pdf = PdfReader(packet)
#             page.merge_page(new_pdf.pages[0])

#         writer.add_page(page)

#     output_stream = io.BytesIO()
#     writer.write(output_stream)
#     output_stream.seek(0)
    
#     return output_stream






# # ---------------- GOOGLE SHEETS FUNCTION ----------------
# def update_google_sheet(data):
#     """Update Google Sheets with form data"""
#     try:
#       if not GOOGLE_SHEETS_URL or GOOGLE_SHEETS_URL == "https://docs.google.com/spreadsheets/d/1lXsUaB6PXKbTfkabKTunSlhGEvczxI45gjN4C3kZGCc/edit?usp=sharing":
#         return False, "Google Sheets Web App URL not configured. Please deploy your Apps Script as a web app and set the URL."  
#       # Prepare data for Google Sheets (as a row)
#       sheet_data = [
#         data.get('Date', ''),
#         data.get('No_of_POS_Required', ''),
#         data.get('Merchant_Name_Commercial', ''),
#         data.get('Merchant_Name_Legal', ''),
#         data.get('Established_since', ''),
#         data.get('How_long_at_this_location', ''),
#         data.get('Business_Address_Commercial', ''),
#         data.get('City', ''),
#         data.get('Telephone1', ''),
#         data.get('Telephone2', ''),
#         data.get('ContactPerson_Name', ''),
#         data.get('Email_Web', ''),
#         data.get('Business_Address_Legal', ''),
#         data.get('City1', ''),
#         data.get('Telephone3', ''),
#         data.get('Telephone4', ''),
#         data.get('ContactPerson_Name1', ''),
#         data.get('Email_Web1', ''),
#         data.get('Number_of_Outlets', ''),
#         data.get('Annual_Sales_Volume', ''),
#         data.get('Average_Transaction_size', ''),
#         data.get('Legal_Structure', ''),
#         data.get('Name', ''),
#         data.get('Designation', ''),
#         data.get('CNIC_No', ''),
#         data.get('Residence_Address', ''),
#         data.get('DirectorName1', ''),
#         data.get('DirectorName2', ''),
#         data.get('DirectorName3', ''),
#         data.get('CNIC_No1', ''),
#         data.get('CNIC_No2', ''),
#         data.get('CNIC_No3', ''),
#         data.get('NTN', ''),
#         data.get('PaymentMode', ''),
#         data.get('Bank_Name', ''),
#         data.get('IBAN', ''),
#         data.get('AccountTitle', ''),
#         data.get('City2', ''),
#         data.get('Debit_Card_FED', ''),
#         data.get('Credit_Card_FED', ''),
#         data.get('intl_Card_FED', ''),
#         data.get('previous_Credit_Card_acceptance', ''),
#         data.get('If_yes', ''),
#         data.get('Current_Status', ''),
#         data.get('TypeNatureofBusinessCategory', ''),
#         data.get('Account_number', ''),
#         data.get('Branch_name', ''),
#         data.get('Branch_code', ''),
#         data.get('select_outlet', ''),
#         data.get('select_type', '')
#       ] 
#       # Send POST request to Google Apps Script Web App
#       response = requests.post(GOOGLE_SHEETS_URL, json=sheet_data, timeout=10)
#       print("Google Sheets response:", response.text)  # Debug log
#       if response.status_code == 200:
#         try:
#           resp_json = response.json()
#           if resp_json.get("success"):
#             return True, resp_json.get("message", "Data successfully updated to Google Sheets")
#           else:
#             return False, resp_json.get("message", "Google Sheets did not confirm success.")
#         except Exception:
#           return True, "Data successfully updated to Google Sheets (no JSON response)"
#       else:
#         return False, f"Failed to update Google Sheets. Status code: {response.status_code}. Response: {response.text}"
#     except requests.exceptions.RequestException as e:
#       return False, f"Error connecting to Google Sheets: {str(e)}"
#     except Exception as e:
#       return False, f"Unexpected error: {str(e)}"

# # ---------------- HTML FORM TEMPLATE ----------------
# form_html = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Merchant Information Form</title>
#   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
#   <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
#   <style>
#     :root {
#       --primary-color: #2563eb;
#       --secondary-color: #64748b;
#       --success-color: #10b981;
#       --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#       --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
#     }

#     body { 
#       background: var(--background-gradient);
#       min-height: 100vh;
#       font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     .main-container {
#       padding: 1rem;
#       min-height: 100vh;
#       display: flex;
#       align-items: center;
#       justify-content: center;
#     }

#     .form-card {
#       background: rgba(255, 255, 255, 0.95);
#       backdrop-filter: blur(10px);
#       border-radius: 20px;
#       border: 1px solid rgba(255, 255, 255, 0.2);
#       box-shadow: var(--card-shadow);
#       width: 100%;
#       max-width: 800px;
#       margin: 2rem 0;
#     }

#     .form-header {
#       background: var(--primary-color);
#       color: white;
#       padding: 2rem;
#       border-radius: 20px 20px 0 0;
#       text-align: center;
#       position: relative;
#       overflow: hidden;
#     }

#     .form-header::before {
#       content: '';
#       position: absolute;
#       top: 0;
#       left: 0;
#       right: 0;
#       bottom: 0;
#       background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
#     }

#     .form-header h2 {
#       margin: 0;
#       font-weight: 700;
#       font-size: clamp(1.5rem, 4vw, 2rem);
#       position: relative;
#       z-index: 1;
#     }

#     .form-header .subtitle {
#       margin-top: 0.5rem;
#       opacity: 0.9;
#       font-size: clamp(0.9rem, 2.5vw, 1.1rem);
#       position: relative;
#       z-index: 1;
#     }

#     .form-body {
#       padding: 2rem;
#     }

#     .section-header {
#       color: var(--primary-color);
#       font-weight: 600;
#       font-size: 1.25rem;
#       margin: 2rem 0 1rem 0;
#       padding-bottom: 0.5rem;
#       border-bottom: 2px solid #e2e8f0;
#       display: flex;
#       align-items: center;
#       gap: 0.5rem;
#     }

#     .section-header:first-child {
#       margin-top: 0;
#     }

#     .form-control, .form-select {
#       border: 2px solid #e2e8f0;
#       border-radius: 10px;
#       padding: 0.75rem 1rem;
#       font-size: 1rem;
#       transition: all 0.3s ease;
#       background-color: #fafafa;
#     }

#     .form-control:focus, .form-select:focus {
#       border-color: var(--primary-color);
#       box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.25);
#       background-color: white;
#     }

#     .form-label {
#       font-weight: 600;
#       color: var(--secondary-color);
#       margin-bottom: 0.5rem;
#       font-size: 0.95rem;
#     }

#     .required-field::after {
#       content: '*';
#       color: #ef4444;
#       margin-left: 4px;
#     }

#     .btn-submit {
#       background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%);
#       border: none;
#       border-radius: 15px;
#       padding: 1rem 2rem;
#       font-size: 1.1rem;
#       font-weight: 600;
#       color: white;
#       transition: all 0.3s ease;
#       box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
#     }

#     .btn-submit:hover {
#       transform: translateY(-2px);
#       box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
#       background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
#     }

#     .director-card {
#       background: #f8fafc;
#       border: 1px solid #e2e8f0;
#       border-radius: 12px;
#       padding: 1rem;
#       margin-bottom: 1rem;
#     }

#     .director-card .form-control {
#       margin-bottom: 0.5rem;
#     }

#     .director-card:last-child {
#       margin-bottom: 0;
#     }

#     textarea.form-control {
#       resize: vertical;
#       min-height: 100px;
#     }

#     /* Mobile Responsiveness */
#     @media (max-width: 768px) {
#       .main-container {
#         padding: 0.5rem;
#       }
      
#       .form-body {
#         padding: 1.5rem;
#       }
      
#       .form-header {
#         padding: 1.5rem;
#       }
      
#       .section-header {
#         font-size: 1.1rem;
#         flex-direction: column;
#         align-items: flex-start;
#         gap: 0.25rem;
#       }
      
#       .director-card {
#         padding: 0.75rem;
#       }
#     }

#     @media (max-width: 576px) {
#       .form-body {
#         padding: 1rem;
#       }
      
#       .form-header {
#         padding: 1rem;
#       }
      
#       .btn-submit {
#         padding: 0.875rem 1.5rem;
#         font-size: 1rem;
#       }
#     }

#     /* Loading Animation */
#     .loading-overlay {
#       display: none;
#       position: fixed;
#       top: 0;
#       left: 0;
#       width: 100%;
#       height: 100%;
#       background: rgba(0, 0, 0, 0.5);
#       z-index: 9999;
#       justify-content: center;
#       align-items: center;
#     }

#     .spinner {
#       width: 50px;
#       height: 50px;
#       border: 5px solid rgba(255, 255, 255, 0.3);
#       border-top: 5px solid white;
#       border-radius: 50%;
#       animation: spin 1s linear infinite;
#     }

#     @keyframes spin {
#       0% { transform: rotate(0deg); }
#       100% { transform: rotate(360deg); }
#     }
#   </style>
# </head>
# <body>
#   <div class="loading-overlay" id="loadingOverlay">
#     <div class="spinner"></div>
#   </div>

#   <div class="main-container">
#     <div class="form-card">
#       <div class="form-header">
#         <h2><i class="fas fa-store me-2"></i>Merchant Information Form</h2>
#         <p class="subtitle">Complete merchant registration and POS setup</p>
#       </div>
      
#       <div class="form-body">
#         <form method="POST" id="merchantForm">
#           <!-- Basic Info -->
#           <div class="section-header">
#             <i class="fas fa-info-circle"></i>
#             Basic Information
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Date</label>
#               <input type="date" class="form-control" name="Date" required>
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Number of POS Required</label>
#               <input type="number" class="form-control" name="No_of_POS_Required" min="1" max="50" placeholder="e.g., 2">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Merchant Name (Commercial)</label>
#               <input type="text" class="form-control" name="Merchant_Name_Commercial" required placeholder="Trading name">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Merchant Name (Legal)</label>
#               <input type="text" class="form-control" name="Merchant_Name_Legal" required placeholder="Legal registered name">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Established Since</label>
#               <input type="text" class="form-control" name="Established_since" placeholder="e.g., 2018">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">How long at this location?</label>
#               <input type="text" class="form-control" name="How_long_at_this_location" placeholder="e.g., 3 years">
#             </div>
#           </div>

#           <!-- Business Address Commercial -->
#           <div class="section-header">
#             <i class="fas fa-map-marker-alt"></i>
#             Business Address (Commercial)
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label required-field">Address</label>
#             <textarea class="form-control" name="Business_Address_Commercial" required placeholder="Enter complete commercial address"></textarea>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">City</label>
#               <input type="text" class="form-control" name="City" placeholder="e.g., Karachi">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Number of Outlets</label>
#               <input type="number" class="form-control" name="Number_of_Outlets" min="1" placeholder="Total outlets">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Telephone 1</label>
#               <input type="tel" class="form-control" name="Telephone1" required placeholder="e.g., 021-12345678">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Telephone 2</label>
#               <input type="tel" class="form-control" name="Telephone2" placeholder="Alternative number">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Contact Person</label>
#               <input type="text" class="form-control" name="ContactPerson_Name" required placeholder="Contact person name">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Email/Website</label>
#               <input type="text" class="form-control" name="Email_Web" placeholder="email@domain.com">
#             </div>
#           </div>

#           <!-- Business Address Legal -->
#           <div class="section-header">
#             <i class="fas fa-balance-scale"></i>
#             Business Address (Legal)
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label required-field">Legal Address</label>
#             <textarea class="form-control" name="Business_Address_Legal" required placeholder="Enter complete legal address"></textarea>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">City</label>
#               <input type="text" class="form-control" name="City1" placeholder="Legal address city">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Annual Sales Volume</label>
#               <input type="text" class="form-control" name="Annual_Sales_Volume" required placeholder="e.g., PKR 10,000,000">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Telephone 1</label>
#               <input type="tel" class="form-control" name="Telephone3" placeholder="Legal address phone 1">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Telephone 2</label>
#               <input type="tel" class="form-control" name="Telephone4" placeholder="Legal address phone 2">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Contact Person</label>
#               <input type="text" class="form-control" name="ContactPerson_Name1" placeholder="Legal contact person">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Email/Website</label>
#               <input type="text" class="form-control" name="Email_Web1" placeholder="legal@domain.com">
#             </div>
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label">Average Transaction Size</label>
#             <input type="text" class="form-control" name="Average_Transaction_size" placeholder="e.g., PKR 2,500">
#           </div>

#           <!-- Owners/Directors -->
#           <div class="section-header">
#             <i class="fas fa-users"></i>
#             Owner / Directors
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Owner Name</label>
#               <input type="text" class="form-control" name="Name" required placeholder="Full name">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Designation</label>
#               <input type="text" class="form-control" name="Designation" placeholder="e.g., CEO, Owner">
#             </div>
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label required-field">CNIC</label>
#             <input type="text" class="form-control" name="CNIC_No" required placeholder="12345-6789012-3" pattern="[0-9]{5}-[0-9]{7}-[0-9]{1}">
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label required-field">Residence Address</label>
#             <textarea class="form-control" name="Residence_Address" required placeholder="Complete residential address"></textarea>
#           </div>
          
#           <div class="row">
#             <div class="col-lg-4 col-md-6 mb-3">
#               <div class="director-card">
#                 <label class="form-label">Director 1</label>
#                 <input type="text" class="form-control" name="DirectorName1" placeholder="Director name">
#                 <input type="text" class="form-control" name="CNIC_No1" placeholder="CNIC: 12345-6789012-3">
#               </div>
#             </div>
#             <div class="col-lg-4 col-md-6 mb-3">
#               <div class="director-card">
#                 <label class="form-label">Director 2</label>
#                 <input type="text" class="form-control" name="DirectorName2" placeholder="Director name">
#                 <input type="text" class="form-control" name="CNIC_No2" placeholder="CNIC: 12345-6789012-3">
#               </div>
#             </div>
#             <div class="col-lg-4 col-md-6 mb-3">
#               <div class="director-card">
#                 <label class="form-label">Director 3</label>
#                 <input type="text" class="form-control" name="DirectorName3" placeholder="Director name">
#                 <input type="text" class="form-control" name="CNIC_No3" placeholder="CNIC: 12345-6789012-3">
#               </div>
#             </div>
#           </div>

#           <!-- Bank Information -->
#           <div class="section-header">
#             <i class="fas fa-university"></i>
#             Bank Information
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Bank Name</label>
#               <input type="text" class="form-control" name="Bank_Name" required placeholder="e.g., HBL, MCB, UBL">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Account Title</label>
#               <input type="text" class="form-control" name="AccountTitle" required placeholder="Account holder name">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Account Number</label>
#               <input type="text" class="form-control" name="Account_number" required placeholder="Account number">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">IBAN</label>
#               <input type="text" class="form-control" name="IBAN" required placeholder="PK36SCBL0000001123456702" minlength="24"  maxlength="24" pattern="[A-Z0-9]{24}" style="text-transform: uppercase;">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-4 mb-3">
#               <label class="form-label">City</label>
#               <input type="text" class="form-control" name="City2" placeholder="Bank branch city" required>
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label required-field">Branch Name</label>
#               <input type="text" class="form-control" name="Branch_name" required placeholder="Branch name">
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Branch Code</label>
#               <input type="text" class="form-control" name="Branch_code" placeholder="Branch code" required>
#             </div>
#           </div>

#           <!-- Options & Fees -->
#           <div class="section-header">
#             <i class="fas fa-cog"></i>
#             Options & Fees
#           </div>
          
#           <div class="row">
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Debit Card FED (%)</label>
#               <input type="number" class="form-control" name="Debit_Card_FED" step="0.01" placeholder="e.g., 1.5">
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Credit Card FED (%)</label>
#               <input type="number" class="form-control" name="Credit_Card_FED" step="0.01" placeholder="e.g., 2.5">
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">International Card FED (%)</label>
#               <input type="number" class="form-control" name="intl_Card_FED" step="0.01" placeholder="e.g., 3.5">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">NTN</label>
#               <input type="text" class="form-control" name="NTN" placeholder="National Tax Number">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Type / Nature of Business</label>
#               <input type="text" class="form-control" name="TypeNatureofBusinessCategory" placeholder="e.g., Restaurant, Retail">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Outlet Type</label>
#               <select class="form-select" name="select_outlet">
#                 <option value="">Select outlet type</option>
#                 <option value="New Outlet">New Outlet</option>
#                 <option value="Chain Outlet">Chain Outlet</option>
#               </select>
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Business Type</label>
#               <select class="form-select" name="select_type">
#                 <option value="">Select business type</option>
#                 <option value="POS">POS</option>
#                 <option value="Ecommerce">Ecommerce</option>
#               </select>
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Legal Structure</label>
#               <select class="form-select" name="Legal_Structure">
#                 <option value="">Select legal structure</option>
#                 <option value="Proprietorship">Proprietorship</option>
#                 <option value="Partnership (Registered/Unregistered)">Partnership</option>
#                 <option value="Pvt Ltd Co.">Pvt Ltd Co.</option>
#                 <option value="Public Ltd Clubs">Public Ltd Clubs</option>
#                 <option value="Others">Others</option>
#               </select>
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Payment Mode</label>
#               <select class="form-select" name="PaymentMode">
#                 <option value="">Select payment mode</option>
#                 <option value="Direct Credit">Direct Credit</option>
#                 <option value="Cheque">Cheque</option>
#                 <option value="IBFT">IBFT</option>
#               </select>
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Previous Credit Card Acceptance</label>
#               <select class="form-select" name="previous_Credit_Card_acceptance">
#                 <option value="">Select</option>
#                 <option value="Yes">Yes</option>
#                 <option value="No">No</option>
#               </select>
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">If Yes (Bank)</label>
#               <select class="form-select" name="If_yes">
#                 <option value="">Select previous bank</option>
#                 <option value="MCB">MCB</option>
#                 <option value="HBL">HBL</option>
#                 <option value="BAFL">BAFL</option>
#                 <option value="MBL">MBL</option>
#                 <option value="Keenu">Keenu</option>
#               </select>
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Current Status</label>
#               <select class="form-select" name="Current_Status">
#                 <option value="">Select status</option>
#                 <option value="Active">Active</option>
#                 <option value="Terminated">Terminated</option>
#               </select>
#             </div>
#           </div>

#           <!-- Submit Button -->
#           <div class="text-center mt-4">
#             <button type="submit" class="btn btn-submit">
#               <i class="fas fa-file-pdf me-2"></i>Generate PDF Document
#             </button>
#           </div>
#         </form>
#       </div>
#     </div>
#   </div>

#   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
#   <script>
#     // Form validation and submission
#     document.getElementById('merchantForm').addEventListener('submit', function(e) {
#       const loadingOverlay = document.getElementById('loadingOverlay');
#       loadingOverlay.style.display = 'flex';
#     });

#     // Auto-format CNIC inputs
#     document.querySelectorAll('input[name*="CNIC"]').forEach(input => {
#       input.addEventListener('input', function(e) {
#         let value = e.target.value.replace(/\D/g, '');
#         if (value.length >= 5) {
#           value = value.substring(0, 5) + '-' + value.substring(5);
#         }
#         if (value.length >= 13) {
#           value = value.substring(0, 13) + '-' + value.substring(13, 14);
#         }
#         e.target.value = value;
#       });
#     });

#     // Set today's date as default
#     document.querySelector('input[name="Date"]').value = new Date().toISOString().split('T')[0];
#   </script>
# </body>
# </html>

# """

# # ---------------- SUCCESS PAGE TEMPLATE ----------------
# success_html = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Submission Successful</title>
#   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
#   <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
#   <style>
#     :root {
#       --primary-color: #2563eb;
#       --success-color: #10b981;
#       --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#       --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
#     }

#     body { 
#       background: var(--background-gradient);
#       min-height: 100vh;
#       font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     .main-container {
#       padding: 2rem;
#       min-height: 100vh;
#       display: flex;
#       align-items: center;
#       justify-content: center;
#     }

#     .success-card {
#       background: rgba(255, 255, 255, 0.95);
#       backdrop-filter: blur(10px);
#       border-radius: 20px;
#       border: 1px solid rgba(255, 255, 255, 0.2);
#       box-shadow: var(--card-shadow);
#       width: 100%;
#       max-width: 600px;
#       text-align: center;
#       overflow: hidden;
#     }

#     .success-header {
#       background: var(--success-color);
#       color: white;
#       padding: 3rem 2rem;
#       position: relative;
#     }

#     .success-header::before {
#       content: '';
#       position: absolute;
#       top: 0;
#       left: 0;
#       right: 0;
#       bottom: 0;
#       background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
#     }

#     .success-icon {
#       font-size: 4rem;
#       margin-bottom: 1rem;
#       position: relative;
#       z-index: 1;
#       animation: checkmark 0.6s ease-in-out;
#     }

#     @keyframes checkmark {
#       0% { transform: scale(0); }
#       50% { transform: scale(1.2); }
#       100% { transform: scale(1); }
#     }

#     .success-title {
#       font-size: 2rem;
#       font-weight: 700;
#       margin: 0;
#       position: relative;
#       z-index: 1;
#     }

#     .success-subtitle {
#       margin-top: 0.5rem;
#       opacity: 0.9;
#       font-size: 1.1rem;
#       position: relative;
#       z-index: 1;
#     }

#     .success-body {
#       padding: 2rem;
#     }

#     .success-message {
#       font-size: 1.1rem;
#       color: #374151;
#       margin-bottom: 2rem;
#     }

#     .btn-primary {
#       background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%);
#       border: none;
#       border-radius: 15px;
#       padding: 1rem 2rem;
#       font-size: 1.1rem;
#       font-weight: 600;
#       color: white;
#       transition: all 0.3s ease;
#       box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
#       margin: 0.5rem;
#     }

#     .btn-primary:hover {
#       transform: translateY(-2px);
#       box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
#       background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
#     }

#     .btn-success {
#       background: linear-gradient(135deg, var(--success-color) 0%, #059669 100%);
#       border: none;
#       border-radius: 15px;
#       padding: 1rem 2rem;
#       font-size: 1.1rem;
#       font-weight: 600;
#       color: white;
#       transition: all 0.3s ease;
#       box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
#       margin: 0.5rem;
#     }

#     .btn-success:hover {
#       transform: translateY(-2px);
#       box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
#       background: linear-gradient(135deg, #059669 0%, #047857 100%);
#     }

#     .alert {
#       border-radius: 10px;
#       border: none;
#       margin-bottom: 2rem;
#     }

#     .alert-info {
#       background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
#       color: #0277bd;
#     }

#     .alert-success {
#       background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
#       color: #2e7d32;
#     }

#     .alert-warning {
#       background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%);
#       color: #f57c00;
#     }

#     .info-section {
#       background: #f8fafc;
#       border-radius: 15px;
#       padding: 1.5rem;
#       margin: 1.5rem 0;
#       border: 1px solid #e2e8f0;
#     }

#     .info-title {
#       font-weight: 600;
#       color: var(--primary-color);
#       margin-bottom: 1rem;
#       font-size: 1.1rem;
#     }

#     .info-item {
#       display: flex;
#       justify-content: space-between;
#       margin-bottom: 0.5rem;
#       padding: 0.25rem 0;
#     }

#     .info-label {
#       font-weight: 500;
#       color: #6b7280;
#     }

#     .info-value {
#       font-weight: 600;
#       color: #374151;
#     }

#     /* Loading Animation for buttons */
#     .btn-loading {
#       position: relative;
#       color: transparent !important;
#     }

#     .btn-loading::after {
#       content: '';
#       position: absolute;
#       width: 20px;
#       height: 20px;
#       top: 50%;
#       left: 50%;
#       margin-left: -10px;
#       margin-top: -10px;
#       border: 2px solid rgba(255,255,255,0.3);
#       border-top: 2px solid white;
#       border-radius: 50%;
#       animation: spin 1s linear infinite;
#     }

#     @keyframes spin {
#       0% { transform: rotate(0deg); }
#       100% { transform: rotate(360deg); }
#     }

#     /* Mobile Responsiveness */
#     @media (max-width: 768px) {
#       .main-container {
#         padding: 1rem;
#       }
      
#       .success-header {
#         padding: 2rem 1rem;
#       }
      
#       .success-body {
#         padding: 1.5rem;
#       }
      
#       .success-icon {
#         font-size: 3rem;
#       }
      
#       .success-title {
#         font-size: 1.5rem;
#       }
      
#       .btn-primary, .btn-success {
#         padding: 0.875rem 1.5rem;
#         font-size: 1rem;
#         display: block;
#         width: 100%;
#         margin: 0.5rem 0;
#       }
#     }
#   </style>
# </head>
# <body>
#   <div class="main-container">
#     <div class="success-card">
#       <div class="success-header">
#         <div class="success-icon">
#           <i class="fas fa-check-circle"></i>
#         </div>
#         <h1 class="success-title">Submission Done!</h1>
#         <p class="success-subtitle">Your merchant information has been processed successfully</p>
#       </div>
      
#       <div class="success-body">
#         <div class="success-message">
#           <strong>Congratulations!</strong> Your merchant registration form has been submitted and PDF document has been generated successfully.
#         </div>

#         {% if pdf_generated %}
#         <div class="alert alert-success">
#           <i class="fas fa-file-pdf me-2"></i>
#           <strong>PDF Generated:</strong> {{ pdf_filename }}
#         </div>
#         <a href="/download/{{ pdf_filename }}" class="btn btn-success mb-2">
#           <i class="fas fa-download me-2"></i>Download PDF
#         </a>
#         {% endif %}

#         <div class="info-section">
#           <div class="info-title">
#             <i class="fas fa-info-circle me-2"></i>Submission Details
#           </div>
#           <div class="info-item">
#             <span class="info-label">Merchant Name:</span>
#             <span class="info-value">{{ merchant_name }}</span>
#           </div>
#           <div class="info-item">
#             <span class="info-label">Submission Date:</span>
#             <span class="info-value">{{ submission_date }}</span>
#           </div>
#           <div class="info-item">
#             <span class="info-label">POS Required:</span>
#             <span class="info-value">{{ pos_required }}</span>
#           </div>
#         </div>

#         <div id="alertContainer"></div>

#         <div class="d-flex flex-wrap justify-content-center">
#           <a href="/" class="btn btn-primary">
#             <i class="fas fa-plus me-2"></i>Back to New Form
#           </a>
#           <button id="updateGoogleSheet" class="btn btn-success" onclick="updateToGoogleSheet()">
#             <i class="fas fa-upload me-2"></i>Update Data to Google Sheet
#           </button>
#         </div>

#         <div class="alert alert-info mt-3">
#           <i class="fas fa-lightbulb me-2"></i>
#           <strong>Next Steps:</strong> Your PDF document is ready for review. Click "Update Data to Google Sheet" to sync your information with the database.
#         </div>
#       </div>
#     </div>
#   </div>

#   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
#   <script>
#     let isUpdating = false;

#     function updateToGoogleSheet() {
#       if (isUpdating) return;
      
#       isUpdating = true;
#       const button = document.getElementById('updateGoogleSheet');
#       const alertContainer = document.getElementById('alertContainer');
      
#       // Add loading state
#       button.classList.add('btn-loading');
#       button.disabled = true;
      
#       // Clear previous alerts
#       alertContainer.innerHTML = '';
      
#       fetch('/update-google-sheet', {
#         method: 'POST',
#         headers: {
#           'Content-Type': 'application/json',
#         }
#       })
#       .then(response => response.json())
#       .then(data => {
#         // Remove loading state
#         button.classList.remove('btn-loading');
#         button.disabled = false;
#         isUpdating = false;
        
#         if (data.success) {
#           alertContainer.innerHTML = `
#             <div class="alert alert-success">
#               <i class="fas fa-check-circle me-2"></i>
#               <strong>Success!</strong> ${data.message}
#             </div>
#           `;
          
#           // Disable button after successful update
#           button.innerHTML = '<i class="fas fa-check me-2"></i>Data Updated Successfully';
#           button.disabled = true;
#           button.classList.remove('btn-success');
#           button.classList.add('btn-secondary');
#         } else {
#           alertContainer.innerHTML = `
#             <div class="alert alert-warning">
#               <i class="fas fa-exclamation-triangle me-2"></i>
#               <strong>Error:</strong> ${data.message}
#             </div>
#           `;
#         }
#       })
#       .catch(error => {
#         // Remove loading state
#         button.classList.remove('btn-loading');
#         button.disabled = false;
#         isUpdating = false;
        
#         alertContainer.innerHTML = `
#           <div class="alert alert-warning">
#             <i class="fas fa-exclamation-triangle me-2"></i>
#             <strong>Network Error:</strong> Unable to connect to Google Sheets. Please check your internet connection and try again.
#           </div>
#         `;
#       });
#     }
#   </script>
  
# </body>
# </html>
# """

# # ---------------- ROUTES ----------------
# @app.route("/", methods=["GET", "POST"])


# def index():
#     if request.method == "POST":
#         # Store form data in session for later use
#         form_data = {}
#         for field in request.form:
#             form_data[field] = request.form.get(field)
        
#         session['form_data'] = form_data
        
#         # Process PDF generation (same as before)
#         select_outlet = request.form.get("select_outlet")
#         select_type = request.form.get("select_type")
#         Date = request.form.get("Date")
#         No_of_POS_Required = request.form.get("No_of_POS_Required")
#         Merchant_Name_Commercial = request.form.get("Merchant_Name_Commercial")
#         Merchant_Name_Legal = request.form.get("Merchant_Name_Legal")
#         Established_since = request.form.get("Established_since")
#         How_long_at_this_location = request.form.get("How_long_at_this_location")
#         Business_Address_Commercial = request.form.get("Business_Address_Commercial")
#         City = request.form.get("City")
#         Telephone1 = request.form.get("Telephone1")
#         Telephone2 = request.form.get("Telephone2")
#         ContactPerson_Name = request.form.get("ContactPerson_Name")
#         Email_Web = request.form.get("Email_Web")
#         Business_Address_Legal = request.form.get("Business_Address_Legal")
#         City1 = request.form.get("City1")
#         Telephone3 = request.form.get("Telephone3")
#         Telephone4 = request.form.get("Telephone4")
#         ContactPerson_Name1 = request.form.get("ContactPerson_Name1")
#         Email_Web1 = request.form.get("Email_Web1")
#         Number_of_Outlets = request.form.get("Number_of_Outlets")
#         Annual_Sales_Volume = request.form.get("Annual_Sales_Volume")
#         Average_Transaction_size = request.form.get("Average_Transaction_size")
#         Legal_Structure = request.form.get("Legal_Structure")
#         Name = request.form.get("Name")
#         Designation = request.form.get("Designation")
#         CNIC_No = request.form.get("CNIC_No")
#         Residence_Address = request.form.get("Residence_Address")
#         DirectorName1 = request.form.get("DirectorName1")
#         DirectorName2 = request.form.get("DirectorName2")
#         DirectorName3 = request.form.get("DirectorName3")
#         CNIC_No1 = request.form.get("CNIC_No1")
#         CNIC_No2 = request.form.get("CNIC_No2")
#         CNIC_No3 = request.form.get("CNIC_No3")
#         NTN = request.form.get("NTN")
#         PaymentMode = request.form.get("PaymentMode")
#         Bank_Name = request.form.get("Bank_Name")
#         IBAN = request.form.get("IBAN")
#         AccountTitle = request.form.get("AccountTitle")
#         City2 = request.form.get("City2")
#         Debit_Card_FED = request.form.get("Debit_Card_FED")
#         Credit_Card_FED = request.form.get("Credit_Card_FED")
#         intl_Card_FED = request.form.get("intl_Card_FED")
#         previous_Credit_Card_acceptance = request.form.get("previous_Credit_Card_acceptance")
#         If_yes = request.form.get("If_yes")
#         Current_Status = request.form.get("Current_Status")
#         TypeNatureofBusinessCategory = request.form.get("TypeNatureofBusinessCategory")
#         Account_number = request.form.get("Account_number")
#         Branch_name = request.form.get("Branch_name")
#         Branch_code = request.form.get("Branch_code")

#         # Address splitting
#         Business_Address_Commercial_1 = ""
#         Business_Address_Legal_1 = ""
#         if Business_Address_Commercial and len(Business_Address_Commercial) > 62:
#             Business_Address_Commercial_1 = Business_Address_Commercial[62:]
#             Business_Address_Commercial = Business_Address_Commercial[:62]

#         if Business_Address_Legal and len(Business_Address_Legal) > 62:
#             Business_Address_Legal_1 = Business_Address_Legal[62:]
#             Business_Address_Legal = Business_Address_Legal[:62]

#         # Text placements (same as before)
#         texts = [
#             (Date, 480, 465, 0),
#             (No_of_POS_Required, 360, 443, 0),
#             (Merchant_Name_Commercial, 190, 420, 0),
#             (Merchant_Name_Legal, 170, 398, 0),
#             (Established_since, 160, 376, 0),
#             (How_long_at_this_location, 430, 376, 0),
#             (Business_Address_Commercial, 200, 354, 0),
#             (City, 430, 333, 0),
#             (Telephone1, 130, 308, 0),
#             (Telephone2, 380, 308, 0),
#             (ContactPerson_Name, 150, 286, 0),
#             (Email_Web, 370, 286, 0),
#             (Business_Address_Legal, 170, 250, 0),
#             (City1, 430, 228, 0),
#             (Telephone3, 130, 205, 0),
#             (Telephone4, 380, 205, 0),
#             (ContactPerson_Name1, 150, 182, 0),
#             (Email_Web1, 100, 160, 0),
#             (Number_of_Outlets, 200, 136, 0),
#             (Annual_Sales_Volume, 200, 115, 0),
#             (Average_Transaction_size, 250, 94, 0),
#             (TypeNatureofBusinessCategory, 210, 70, 0),
#             (Name, 83, 705, 1),
#             (Designation, 280, 705, 1),
#             (CNIC_No, 440, 705, 1),
#             (Residence_Address, 157, 683, 1),
#             (DirectorName1, 140, 660, 1),
#             (DirectorName2, 140, 640, 1),
#             (DirectorName3, 140, 617, 1),
#             (CNIC_No1, 435, 660, 1),
#             (CNIC_No2, 435, 640, 1),
#             (CNIC_No3, 435, 617, 1),
#             (NTN, 130, 594, 1),
#             (Bank_Name, 110, 548, 1),
#             (IBAN, 122, 520, 1),
#             (AccountTitle, 110, 485, 1),
#             (City2, 405, 485, 1),
#             (Debit_Card_FED, 205, 460, 1),
#             (Credit_Card_FED, 350, 460, 1),
#             (intl_Card_FED, 510, 460, 1),
#         ]

#         # Extra address lines
#         if Business_Address_Commercial_1:
#             texts.append((Business_Address_Commercial_1, 35, 332, 0))

#         if Business_Address_Legal_1:
#             texts.append((Business_Address_Legal_1, 40, 228, 0))

#         # Checkboxes logic (same as before)
#         if select_outlet == "New Outlet":
#             texts.append(("✓", 40, 460, 0))
#         elif select_outlet == "Chain Outlet":
#             texts.append(("✓", 125, 460, 0))

#         if select_type == "POS":
#             texts.append(("✓", 40, 438, 0))
#         elif select_type == "Ecommerce":
#             texts.append(("✓", 137, 438, 0))

#         if Legal_Structure == "Proprietorship":
#             texts.append(("✓", 42, 773, 1))
#         elif Legal_Structure == "Partnership (Registered/Unregistered)":
#             texts.append(("✓", 154, 773, 1))
#         elif Legal_Structure == "Pvt Ltd Co.":
#             texts.append(("✓", 383, 773, 1))
#         elif Legal_Structure == "Public Ltd Clubs":
#             texts.append(("✓", 42, 750, 1))
#         elif Legal_Structure == "Others":
#             texts.append(("✓", 154, 750, 1))

#         if PaymentMode == "Direct Credit":
#             texts.append(("✓", 158, 570, 1))
#         elif PaymentMode == "Cheque":
#             texts.append(("✓", 296, 570, 1))
#         elif PaymentMode == "IBFT":
#             texts.append(("✓", 390, 570, 1))

#         if previous_Credit_Card_acceptance == "Yes":
#             texts.append(("✓", 300, 430, 1))
#         elif previous_Credit_Card_acceptance == "No":
#             texts.append(("✓", 350, 430, 1))

#         if If_yes == "MCB":
#             texts.append(("✓", 157, 405, 1))
#         elif If_yes == "HBL":
#             texts.append(("✓", 225, 405, 1))
#         elif If_yes == "BAFL":
#             texts.append(("✓", 292, 405, 1))
#         elif If_yes == "MBL":
#             texts.append(("✓", 360, 405, 1))
#         elif If_yes == "Keenu":
#             texts.append(("✓", 430, 405, 1))

#         if Current_Status == "Active":
#             texts.append(("✓", 226, 380, 1))
#         elif Current_Status == "Terminated":
#             texts.append(("✓", 293, 380, 1))

#         try:
#             safe_name = re.sub(r'[\\/*?:"<>|]', "_", Merchant_Name_Legal or "merchant")
#             pdf_stream = generate_filled_pdf(texts, safe_name)
#             pdf_path = fr"C:\Users\HP\Desktop\Projects\{safe_name}.pdf"
#             with open(pdf_path, "wb") as f:
#               f.write(pdf_stream.read())
#             session['pdf_generated'] = True
#             session['pdf_filename'] = f"{safe_name}.pdf"
#             session['pdf_error'] = ''
#             return redirect(url_for('success'))
#         except Exception as e:
#             session['pdf_generated'] = False
#             session['pdf_filename'] = ''
#             session['pdf_error'] = str(e)
#         return redirect(url_for('success'))

#     return render_template_string(form_html)

# @app.route("/success")
# def success():
#     form_data = session.get('form_data', {})
    
#     pdf_generated = session.get('pdf_generated', False)
#     pdf_filename = session.get('pdf_filename', '')
#     pdf_error = session.get('pdf_error', '')
#     return render_template_string(success_html,
#       merchant_name=form_data.get('Merchant_Name_Legal', 'N/A'),
#       submission_date=form_data.get('Date', 'N/A'),
#       pos_required=form_data.get('No_of_POS_Required', 'N/A'),
#       pdf_generated=pdf_generated,
#       pdf_filename=pdf_filename,
#       pdf_error=pdf_error
#     )
# @app.route('/download/<filename>')
# def download_pdf(filename):
#   pdf_path = f"C:/Users/HP/Desktop/Projects/{filename}"
#   return send_file(pdf_path, as_attachment=True)

# @app.route("/update-google-sheet", methods=["POST"])
# def update_google_sheet_route():
#     form_data = session.get('form_data', {})
    
#     if not form_data:
#         return {"success": False, "message": "No form data found in session"}
    
#     success, message = update_google_sheet(form_data)
    
#     return {"success": success, "message": message}

# if __name__ == "__main__":
#     # IMPORTANT: Add your Google Sheets URL here
#     GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyN-kwS8MMUohF9-B_J0ANaohOAgWCGfZYJGzvVLLSoh0MipEmsNlQnA0MEcH-tN3nn/exec" 
#     print("=" * 50)
#     print("IMPORTANT: Configure Google Sheets Integration")
#     print("=" * 50)
#     print("1. Create a Google Apps Script web app")
#     print("2. Add your Google Sheets URL to GOOGLE_SHEETS_URL variable")
#     print("3. Make sure your Google Script accepts POST requests")
#     print("=" * 50)
    
#     app.run(debug=True, port=5500)















    
# from flask import Flask, render_template_string, request, send_file, redirect, url_for, session
# from PyPDF2 import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# import io
# import re
# import requests
# import json

# app = Flask(__name__)
# app.secret_key = 'haseeb_key'  # Change this to a random secret key

# # Google Sheets configuration
# GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyN-kwS8MMUohF9-B_J0ANaohOAgWCGfZYJGzvVLLSoh0MipEmsNlQnA0MEcH-tN3nn/exec"  # Replace with your Google Apps Script web app URL

# # ---------------- SAFE TEXT HELPER ----------------
# def safe_text(value):
#     return str(value) if value else ""

# # ---------------- PDF GENERATION FUNCTION ----------------
# # Generate PDF in memory
# def generate_filled_pdf(texts, safe_name):
#     input_pdf_path = r"C:\Users\HP\Desktop\Projects\A4 Merchant Form.pdf"
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     # Group text per page
#     page_texts = {}
#     for text, x, y, page_number in texts:
#         page_texts.setdefault(page_number, []).append((text, x, y))

#     for page_num in range(len(reader.pages)):
#         page = reader.pages[page_num]

#         if page_num in page_texts:
#             packet = io.BytesIO()
#             c = canvas.Canvas(packet, pagesize=letter)
#             for text, x, y in page_texts[page_num]:
#                 c.drawString(x, y, safe_text(text))
#             c.save()

#             packet.seek(0)
#             new_pdf = PdfReader(packet)
#             page.merge_page(new_pdf.pages[0])

#         writer.add_page(page)

#     output_stream = io.BytesIO()
#     writer.write(output_stream)
#     output_stream.seek(0)
    
#     return output_stream






# # ---------------- GOOGLE SHEETS FUNCTION ----------------
# def update_google_sheet(data):
#     """Update Google Sheets with form data"""
#     try:
#       if not GOOGLE_SHEETS_URL or GOOGLE_SHEETS_URL == "https://docs.google.com/spreadsheets/d/1lXsUaB6PXKbTfkabKTunSlhGEvczxI45gjN4C3kZGCc/edit?usp=sharing":
#         return False, "Google Sheets Web App URL not configured. Please deploy your Apps Script as a web app and set the URL."  
#       # Prepare data for Google Sheets (as a row)
#       sheet_data = [
#         data.get('Date', ''),
#         data.get('No_of_POS_Required', ''),
#         data.get('Merchant_Name_Commercial', ''),
#         data.get('Merchant_Name_Legal', ''),
#         data.get('Established_since', ''),
#         data.get('How_long_at_this_location', ''),
#         data.get('Business_Address_Commercial', ''),
#         data.get('City', ''),
#         data.get('Telephone1', ''),
#         data.get('Telephone2', ''),
#         data.get('ContactPerson_Name', ''),
#         data.get('Email_Web', ''),
#         data.get('Business_Address_Legal', ''),
#         data.get('City1', ''),
#         data.get('Telephone3', ''),
#         data.get('Telephone4', ''),
#         data.get('ContactPerson_Name1', ''),
#         data.get('Email_Web1', ''),
#         data.get('Number_of_Outlets', ''),
#         data.get('Annual_Sales_Volume', ''),
#         data.get('Average_Transaction_size', ''),
#         data.get('Legal_Structure', ''),
#         data.get('Name', ''),
#         data.get('Designation', ''),
#         data.get('CNIC_No', ''),
#         data.get('Residence_Address', ''),
#         data.get('DirectorName1', ''),
#         data.get('DirectorName2', ''),
#         data.get('DirectorName3', ''),
#         data.get('CNIC_No1', ''),
#         data.get('CNIC_No2', ''),
#         data.get('CNIC_No3', ''),
#         data.get('NTN', ''),
#         data.get('PaymentMode', ''),
#         data.get('Bank_Name', ''),
#         data.get('IBAN', ''),
#         data.get('AccountTitle', ''),
#         data.get('City2', ''),
#         data.get('Debit_Card_FED', ''),
#         data.get('Credit_Card_FED', ''),
#         data.get('intl_Card_FED', ''),
#         data.get('previous_Credit_Card_acceptance', ''),
#         data.get('If_yes', ''),
#         data.get('Current_Status', ''),
#         data.get('TypeNatureofBusinessCategory', ''),
#         data.get('Account_number', ''),
#         data.get('Branch_name', ''),
#         data.get('Branch_code', ''),
#         data.get('select_outlet', ''),
#         data.get('select_type', '')
#       ] 
#       # Send POST request to Google Apps Script Web App
#       response = requests.post(GOOGLE_SHEETS_URL, json=sheet_data, timeout=10)
#       print("Google Sheets response:", response.text)  # Debug log
#       if response.status_code == 200:
#         try:
#           resp_json = response.json()
#           if resp_json.get("success"):
#             return True, resp_json.get("message", "Data successfully updated to Google Sheets")
#           else:
#             return False, resp_json.get("message", "Google Sheets did not confirm success.")
#         except Exception:
#           return True, "Data successfully updated to Google Sheets (no JSON response)"
#       else:
#         return False, f"Failed to update Google Sheets. Status code: {response.status_code}. Response: {response.text}"
#     except requests.exceptions.RequestException as e:
#       return False, f"Error connecting to Google Sheets: {str(e)}"
#     except Exception as e:
#       return False, f"Unexpected error: {str(e)}"

# # ---------------- HTML FORM TEMPLATE ----------------
# form_html = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Merchant Information Form</title>
#   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
#   <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
#   <style>
#     :root {
#       --primary-color: #2563eb;
#       --secondary-color: #64748b;
#       --success-color: #10b981;
#       --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#       --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
#     }

#     body { 
#       background: var(--background-gradient);
#       min-height: 100vh;
#       font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     .main-container {
#       padding: 1rem;
#       min-height: 100vh;
#       display: flex;
#       align-items: center;
#       justify-content: center;
#     }

#     .form-card {
#       background: rgba(255, 255, 255, 0.95);
#       backdrop-filter: blur(10px);
#       border-radius: 20px;
#       border: 1px solid rgba(255, 255, 255, 0.2);
#       box-shadow: var(--card-shadow);
#       width: 100%;
#       max-width: 800px;
#       margin: 2rem 0;
#     }

#     .form-header {
#       background: var(--primary-color);
#       color: white;
#       padding: 2rem;
#       border-radius: 20px 20px 0 0;
#       text-align: center;
#       position: relative;
#       overflow: hidden;
#     }

#     .form-header::before {
#       content: '';
#       position: absolute;
#       top: 0;
#       left: 0;
#       right: 0;
#       bottom: 0;
#       background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
#     }

#     .form-header h2 {
#       margin: 0;
#       font-weight: 700;
#       font-size: clamp(1.5rem, 4vw, 2rem);
#       position: relative;
#       z-index: 1;
#     }

#     .form-header .subtitle {
#       margin-top: 0.5rem;
#       opacity: 0.9;
#       font-size: clamp(0.9rem, 2.5vw, 1.1rem);
#       position: relative;
#       z-index: 1;
#     }

#     .form-body {
#       padding: 2rem;
#     }

#     .section-header {
#       color: var(--primary-color);
#       font-weight: 600;
#       font-size: 1.25rem;
#       margin: 2rem 0 1rem 0;
#       padding-bottom: 0.5rem;
#       border-bottom: 2px solid #e2e8f0;
#       display: flex;
#       align-items: center;
#       gap: 0.5rem;
#     }

#     .section-header:first-child {
#       margin-top: 0;
#     }

#     .form-control, .form-select {
#       border: 2px solid #e2e8f0;
#       border-radius: 10px;
#       padding: 0.75rem 1rem;
#       font-size: 1rem;
#       transition: all 0.3s ease;
#       background-color: #fafafa;
#     }

#     .form-control:focus, .form-select:focus {
#       border-color: var(--primary-color);
#       box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.25);
#       background-color: white;
#     }

#     .form-label {
#       font-weight: 600;
#       color: var(--secondary-color);
#       margin-bottom: 0.5rem;
#       font-size: 0.95rem;
#     }

#     .required-field::after {
#       content: '*';
#       color: #ef4444;
#       margin-left: 4px;
#     }

#     .btn-submit {
#       background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%);
#       border: none;
#       border-radius: 15px;
#       padding: 1rem 2rem;
#       font-size: 1.1rem;
#       font-weight: 600;
#       color: white;
#       transition: all 0.3s ease;
#       box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
#     }

#     .btn-submit:hover {
#       transform: translateY(-2px);
#       box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
#       background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
#     }

#     .director-card {
#       background: #f8fafc;
#       border: 1px solid #e2e8f0;
#       border-radius: 12px;
#       padding: 1rem;
#       margin-bottom: 1rem;
#     }

#     .director-card .form-control {
#       margin-bottom: 0.5rem;
#     }

#     .director-card:last-child {
#       margin-bottom: 0;
#     }

#     textarea.form-control {
#       resize: vertical;
#       min-height: 100px;
#     }

#     /* Mobile Responsiveness */
#     @media (max-width: 768px) {
#       .main-container {
#         padding: 0.5rem;
#       }
      
#       .form-body {
#         padding: 1.5rem;
#       }
      
#       .form-header {
#         padding: 1.5rem;
#       }
      
#       .section-header {
#         font-size: 1.1rem;
#         flex-direction: column;
#         align-items: flex-start;
#         gap: 0.25rem;
#       }
      
#       .director-card {
#         padding: 0.75rem;
#       }
#     }

#     @media (max-width: 576px) {
#       .form-body {
#         padding: 1rem;
#       }
      
#       .form-header {
#         padding: 1rem;
#       }
      
#       .btn-submit {
#         padding: 0.875rem 1.5rem;
#         font-size: 1rem;
#       }
#     }

#     /* Loading Animation */
#     .loading-overlay {
#       display: none;
#       position: fixed;
#       top: 0;
#       left: 0;
#       width: 100%;
#       height: 100%;
#       background: rgba(0, 0, 0, 0.5);
#       z-index: 9999;
#       justify-content: center;
#       align-items: center;
#     }

#     .spinner {
#       width: 50px;
#       height: 50px;
#       border: 5px solid rgba(255, 255, 255, 0.3);
#       border-top: 5px solid white;
#       border-radius: 50%;
#       animation: spin 1s linear infinite;
#     }

#     @keyframes spin {
#       0% { transform: rotate(0deg); }
#       100% { transform: rotate(360deg); }
#     }
#   </style>
# </head>
# <body>
#   <div class="loading-overlay" id="loadingOverlay">
#     <div class="spinner"></div>
#   </div>

#   <div class="main-container">
#     <div class="form-card">
#       <div class="form-header">
#         <h2><i class="fas fa-store me-2"></i>Merchant Information Form</h2>
#         <p class="subtitle">Complete merchant registration and POS setup</p>
#       </div>
      
#       <div class="form-body">
#         <form method="POST" id="merchantForm">
#           <!-- Basic Info -->
#           <div class="section-header">
#             <i class="fas fa-info-circle"></i>
#             Basic Information
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Date</label>
#               <input type="date" class="form-control" name="Date" required>
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Number of POS Required</label>
#               <input type="number" class="form-control" name="No_of_POS_Required" min="1" max="50" placeholder="e.g., 2">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Merchant Name (Commercial)</label>
#               <input type="text" class="form-control" name="Merchant_Name_Commercial" required placeholder="Trading name">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Merchant Name (Legal)</label>
#               <input type="text" class="form-control" name="Merchant_Name_Legal" required placeholder="Legal registered name">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Established Since</label>
#               <input type="text" class="form-control" name="Established_since" placeholder="e.g., 2018">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">How long at this location?</label>
#               <input type="text" class="form-control" name="How_long_at_this_location" placeholder="e.g., 3 years">
#             </div>
#           </div>

#           <!-- Business Address Commercial -->
#           <div class="section-header">
#             <i class="fas fa-map-marker-alt"></i>
#             Business Address (Commercial)
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label required-field">Address</label>
#             <textarea class="form-control" name="Business_Address_Commercial" required placeholder="Enter complete commercial address"></textarea>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">City</label>
#               <input type="text" class="form-control" name="City" placeholder="e.g., Karachi">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Number of Outlets</label>
#               <input type="number" class="form-control" name="Number_of_Outlets" min="1" placeholder="Total outlets">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Telephone 1</label>
#               <input type="tel" class="form-control" name="Telephone1" required placeholder="e.g., 021-12345678">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Telephone 2</label>
#               <input type="tel" class="form-control" name="Telephone2" placeholder="Alternative number">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Contact Person</label>
#               <input type="text" class="form-control" name="ContactPerson_Name" required placeholder="Contact person name">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Email/Website</label>
#               <input type="text" class="form-control" name="Email_Web" placeholder="email@domain.com">
#             </div>
#           </div>

#           <!-- Business Address Legal -->
#           <div class="section-header">
#             <i class="fas fa-balance-scale"></i>
#             Business Address (Legal)
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label required-field">Legal Address</label>
#             <textarea class="form-control" name="Business_Address_Legal" required placeholder="Enter complete legal address"></textarea>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">City</label>
#               <input type="text" class="form-control" name="City1" placeholder="Legal address city">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Annual Sales Volume</label>
#               <input type="text" class="form-control" name="Annual_Sales_Volume" required placeholder="e.g., PKR 10,000,000">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Telephone 1</label>
#               <input type="tel" class="form-control" name="Telephone3" placeholder="Legal address phone 1">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Telephone 2</label>
#               <input type="tel" class="form-control" name="Telephone4" placeholder="Legal address phone 2">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Contact Person</label>
#               <input type="text" class="form-control" name="ContactPerson_Name1" placeholder="Legal contact person">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Email/Website</label>
#               <input type="text" class="form-control" name="Email_Web1" placeholder="legal@domain.com">
#             </div>
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label">Average Transaction Size</label>
#             <input type="text" class="form-control" name="Average_Transaction_size" placeholder="e.g., PKR 2,500">
#           </div>

#           <!-- Owners/Directors -->
#           <div class="section-header">
#             <i class="fas fa-users"></i>
#             Owner / Directors
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Owner Name</label>
#               <input type="text" class="form-control" name="Name" required placeholder="Full name">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Designation</label>
#               <input type="text" class="form-control" name="Designation" placeholder="e.g., CEO, Owner">
#             </div>
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label required-field">CNIC</label>
#             <input type="text" class="form-control" name="CNIC_No" required placeholder="12345-6789012-3" pattern="[0-9]{5}-[0-9]{7}-[0-9]{1}">
#           </div>
          
#           <div class="mb-3">
#             <label class="form-label required-field">Residence Address</label>
#             <textarea class="form-control" name="Residence_Address" required placeholder="Complete residential address"></textarea>
#           </div>
          
#           <div class="row">
#             <div class="col-lg-4 col-md-6 mb-3">
#               <div class="director-card">
#                 <label class="form-label">Director 1</label>
#                 <input type="text" class="form-control" name="DirectorName1" placeholder="Director name">
#                 <input type="text" class="form-control" name="CNIC_No1" placeholder="CNIC: 12345-6789012-3">
#               </div>
#             </div>
#             <div class="col-lg-4 col-md-6 mb-3">
#               <div class="director-card">
#                 <label class="form-label">Director 2</label>
#                 <input type="text" class="form-control" name="DirectorName2" placeholder="Director name">
#                 <input type="text" class="form-control" name="CNIC_No2" placeholder="CNIC: 12345-6789012-3">
#               </div>
#             </div>
#             <div class="col-lg-4 col-md-6 mb-3">
#               <div class="director-card">
#                 <label class="form-label">Director 3</label>
#                 <input type="text" class="form-control" name="DirectorName3" placeholder="Director name">
#                 <input type="text" class="form-control" name="CNIC_No3" placeholder="CNIC: 12345-6789012-3">
#               </div>
#             </div>
#           </div>

#           <!-- Bank Information -->
#           <div class="section-header">
#             <i class="fas fa-university"></i>
#             Bank Information
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Bank Name</label>
#               <input type="text" class="form-control" name="Bank_Name" required placeholder="e.g., HBL, MCB, UBL">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Account Title</label>
#               <input type="text" class="form-control" name="AccountTitle" required placeholder="Account holder name">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">Account Number</label>
#               <input type="text" class="form-control" name="Account_number" required placeholder="Account number">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label required-field">IBAN</label>
#               <input type="text" class="form-control" name="IBAN" required placeholder="PK36SCBL0000001123456702" minlength="24"  maxlength="24" style="text-transform: uppercase;">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-4 mb-3">
#               <label class="form-label" required-field>City</label>
#               <input type="text" class="form-control" name="City2" placeholder="Bank branch city" required>
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label required-field">Branch Name</label>
#               <input type="text" class="form-control" name="Branch_name" required placeholder="Branch name">
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label" required-field>Branch Code</label>
#               <input type="text" class="form-control" name="Branch_code" placeholder="Branch code" required>
#             </div>
#           </div>

#           <!-- Options & Fees -->
#           <div class="section-header">
#             <i class="fas fa-cog"></i>
#             Options & Fees
#           </div>
          
#           <div class="row">
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Debit Card FED (%)</label>
#               <input type="number" class="form-control" name="Debit_Card_FED" step="0.01" placeholder="e.g., 1.5">
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Credit Card FED (%)</label>
#               <input type="number" class="form-control" name="Credit_Card_FED" step="0.01" placeholder="e.g., 2.5">
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">International Card FED (%)</label>
#               <input type="number" class="form-control" name="intl_Card_FED" step="0.01" placeholder="e.g., 3.5">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">NTN</label>
#               <input type="text" class="form-control" name="NTN" placeholder="National Tax Number">
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Type / Nature of Business</label>
#               <input type="text" class="form-control" name="TypeNatureofBusinessCategory" placeholder="e.g., Restaurant, Retail">
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Outlet Type</label>
#               <select class="form-select" name="select_outlet">
#                 <option value="">Select outlet type</option>
#                 <option value="New Outlet">New Outlet</option>
#                 <option value="Chain Outlet">Chain Outlet</option>
#               </select>
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Business Type</label>
#               <select class="form-select" name="select_type">
#                 <option value="">Select business type</option>
#                 <option value="POS">POS</option>
#                 <option value="Ecommerce">Ecommerce</option>
#               </select>
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Legal Structure</label>
#               <select class="form-select" name="Legal_Structure">
#                 <option value="">Select legal structure</option>
#                 <option value="Proprietorship">Proprietorship</option>
#                 <option value="Partnership (Registered/Unregistered)">Partnership</option>
#                 <option value="Pvt Ltd Co.">Pvt Ltd Co.</option>
#                 <option value="Public Ltd Clubs">Public Ltd Clubs</option>
#                 <option value="Others">Others</option>
#               </select>
#             </div>
#             <div class="col-md-6 mb-3">
#               <label class="form-label">Payment Mode</label>
#               <select class="form-select" name="PaymentMode">
#                 <option value="">Select payment mode</option>
#                 <option value="Direct Credit">Direct Credit</option>
#                 <option value="Cheque">Cheque</option>
#                 <option value="IBFT">IBFT</option>
#               </select>
#             </div>
#           </div>
          
#           <div class="row">
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Previous Credit Card Acceptance</label>
#               <select class="form-select" name="previous_Credit_Card_acceptance">
#                 <option value="">Select</option>
#                 <option value="Yes">Yes</option>
#                 <option value="No">No</option>
#               </select>
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">If Yes (Bank)</label>
#               <select class="form-select" name="If_yes">
#                 <option value="">Select previous bank</option>
#                 <option value="MCB">MCB</option>
#                 <option value="HBL">HBL</option>
#                 <option value="BAFL">BAFL</option>
#                 <option value="MBL">MBL</option>
#                 <option value="Keenu">Keenu</option>
#               </select>
#             </div>
#             <div class="col-md-4 mb-3">
#               <label class="form-label">Current Status</label>
#               <select class="form-select" name="Current_Status">
#                 <option value="">Select status</option>
#                 <option value="Active">Active</option>
#                 <option value="Terminated">Terminated</option>
#               </select>
#             </div>
#           </div>

#           <!-- Submit Button -->
#           <div class="text-center mt-4">
#             <button type="submit" class="btn btn-submit">
#               <i class="fas fa-file-pdf me-2"></i>Generate PDF Document
#             </button>
#           </div>
#         </form>
#       </div>
#     </div>
#   </div>

#   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
#   <script>
#     // Form validation and submission
#     document.getElementById('merchantForm').addEventListener('submit', function(e) {
#       const loadingOverlay = document.getElementById('loadingOverlay');
#       loadingOverlay.style.display = 'flex';
#     });

#     // Auto-format CNIC inputs
#     document.querySelectorAll('input[name*="CNIC"]').forEach(input => {
#       input.addEventListener('input', function(e) {
#         let value = e.target.value.replace(/\D/g, '');
#         if (value.length >= 5) {
#           value = value.substring(0, 5) + '-' + value.substring(5);
#         }
#         if (value.length >= 13) {
#           value = value.substring(0, 13) + '-' + value.substring(13, 14);
#         }
#         e.target.value = value;
#       });
#     });

#     // Set today's date as default
#     document.querySelector('input[name="Date"]').value = new Date().toISOString().split('T')[0];
#   </script>
# </body>
# </html>

# """

# # ---------------- SUCCESS PAGE TEMPLATE ----------------
# success_html = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Submission Successful</title>
#   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
#   <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
#   <style>
#     :root {
#       --primary-color: #2563eb;
#       --success-color: #10b981;
#       --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#       --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
#     }

#     body { 
#       background: var(--background-gradient);
#       min-height: 100vh;
#       font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     .main-container {
#       padding: 2rem;
#       min-height: 100vh;
#       display: flex;
#       align-items: center;
#       justify-content: center;
#     }

#     .success-card {
#       background: rgba(255, 255, 255, 0.95);
#       backdrop-filter: blur(10px);
#       border-radius: 20px;
#       border: 1px solid rgba(255, 255, 255, 0.2);
#       box-shadow: var(--card-shadow);
#       width: 100%;
#       max-width: 600px;
#       text-align: center;
#       overflow: hidden;
#     }

#     .success-header {
#       background: var(--success-color);
#       color: white;
#       padding: 3rem 2rem;
#       position: relative;
#     }

#     .success-header::before {
#       content: '';
#       position: absolute;
#       top: 0;
#       left: 0;
#       right: 0;
#       bottom: 0;
#       background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
#     }

#     .success-icon {
#       font-size: 4rem;
#       margin-bottom: 1rem;
#       position: relative;
#       z-index: 1;
#       animation: checkmark 0.6s ease-in-out;
#     }

#     @keyframes checkmark {
#       0% { transform: scale(0); }
#       50% { transform: scale(1.2); }
#       100% { transform: scale(1); }
#     }

#     .success-title {
#       font-size: 2rem;
#       font-weight: 700;
#       margin: 0;
#       position: relative;
#       z-index: 1;
#     }

#     .success-subtitle {
#       margin-top: 0.5rem;
#       opacity: 0.9;
#       font-size: 1.1rem;
#       position: relative;
#       z-index: 1;
#     }

#     .success-body {
#       padding: 2rem;
#     }

#     .success-message {
#       font-size: 1.1rem;
#       color: #374151;
#       margin-bottom: 2rem;
#     }

#     .btn-primary {
#       background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%);
#       border: none;
#       border-radius: 15px;
#       padding: 1rem 2rem;
#       font-size: 1.1rem;
#       font-weight: 600;
#       color: white;
#       transition: all 0.3s ease;
#       box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
#       margin: 0.5rem;
#     }

#     .btn-primary:hover {
#       transform: translateY(-2px);
#       box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
#       background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
#     }

#     .btn-success {
#       background: linear-gradient(135deg, var(--success-color) 0%, #059669 100%);
#       border: none;
#       border-radius: 15px;
#       padding: 1rem 2rem;
#       font-size: 1.1rem;
#       font-weight: 600;
#       color: white;
#       transition: all 0.3s ease;
#       box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
#       margin: 0.5rem;
#     }

#     .btn-success:hover {
#       transform: translateY(-2px);
#       box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
#       background: linear-gradient(135deg, #059669 0%, #047857 100%);
#     }

#     .alert {
#       border-radius: 10px;
#       border: none;
#       margin-bottom: 2rem;
#     }

#     .alert-info {
#       background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
#       color: #0277bd;
#     }

#     .alert-success {
#       background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
#       color: #2e7d32;
#     }

#     .alert-warning {
#       background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%);
#       color: #f57c00;
#     }

#     .info-section {
#       background: #f8fafc;
#       border-radius: 15px;
#       padding: 1.5rem;
#       margin: 1.5rem 0;
#       border: 1px solid #e2e8f0;
#     }

#     .info-title {
#       font-weight: 600;
#       color: var(--primary-color);
#       margin-bottom: 1rem;
#       font-size: 1.1rem;
#     }

#     .info-item {
#       display: flex;
#       justify-content: space-between;
#       margin-bottom: 0.5rem;
#       padding: 0.25rem 0;
#     }

#     .info-label {
#       font-weight: 500;
#       color: #6b7280;
#     }

#     .info-value {
#       font-weight: 600;
#       color: #374151;
#     }

#     /* Loading Animation for buttons */
#     .btn-loading {
#       position: relative;
#       color: transparent !important;
#     }

#     .btn-loading::after {
#       content: '';
#       position: absolute;
#       width: 20px;
#       height: 20px;
#       top: 50%;
#       left: 50%;
#       margin-left: -10px;
#       margin-top: -10px;
#       border: 2px solid rgba(255,255,255,0.3);
#       border-top: 2px solid white;
#       border-radius: 50%;
#       animation: spin 1s linear infinite;
#     }

#     @keyframes spin {
#       0% { transform: rotate(0deg); }
#       100% { transform: rotate(360deg); }
#     }

#     /* Mobile Responsiveness */
#     @media (max-width: 768px) {
#       .main-container {
#         padding: 1rem;
#       }
      
#       .success-header {
#         padding: 2rem 1rem;
#       }
      
#       .success-body {
#         padding: 1.5rem;
#       }
      
#       .success-icon {
#         font-size: 3rem;
#       }
      
#       .success-title {
#         font-size: 1.5rem;
#       }
      
#       .btn-primary, .btn-success {
#         padding: 0.875rem 1.5rem;
#         font-size: 1rem;
#         display: block;
#         width: 100%;
#         margin: 0.5rem 0;
#       }
#     }
#   </style>
# </head>
# <body>
#   <div class="main-container">
#     <div class="success-card">
#       <div class="success-header">
#         <div class="success-icon">
#           <i class="fas fa-check-circle"></i>
#         </div>
#         <h1 class="success-title">Submission Done!</h1>
#         <p class="success-subtitle">Your merchant information has been processed successfully</p>
#       </div>
      
#       <div class="success-body">
#         <div class="success-message">
#           <strong>Congratulations!</strong> Your merchant registration form has been submitted and PDF document has been generated successfully.
#         </div>

#         {% if pdf_generated %}
#         <div class="alert alert-success">
#           <i class="fas fa-file-pdf me-2"></i>
#           <strong>PDF Generated:</strong> {{ pdf_filename }}
#         </div>
#         <a href="/download/{{ pdf_filename }}" class="btn btn-success mb-2">
#           <i class="fas fa-download me-2"></i>Download PDF
#         </a>
#         {% endif %}

#         <div class="info-section">
#           <div class="info-title">
#             <i class="fas fa-info-circle me-2"></i>Submission Details
#           </div>
#           <div class="info-item">
#             <span class="info-label">Merchant Name:</span>
#             <span class="info-value">{{ merchant_name }}</span>
#           </div>
#           <div class="info-item">
#             <span class="info-label">Submission Date:</span>
#             <span class="info-value">{{ submission_date }}</span>
#           </div>
#           <div class="info-item">
#             <span class="info-label">POS Required:</span>
#             <span class="info-value">{{ pos_required }}</span>
#           </div>
#         </div>

#         <div id="alertContainer"></div>

#         <div class="d-flex flex-wrap justify-content-center">
#           <a href="/" class="btn btn-primary">
#             <i class="fas fa-plus me-2"></i>Back to New Form
#           </a>
#           <button id="updateGoogleSheet" class="btn btn-success" onclick="updateToGoogleSheet()">
#             <i class="fas fa-upload me-2"></i>Update Data to Google Sheet
#           </button>
#         </div>

#         <div class="alert alert-info mt-3">
#           <i class="fas fa-lightbulb me-2"></i>
#           <strong>Next Steps:</strong> Your PDF document is ready for review. Click "Update Data to Google Sheet" to sync your information with the database.
#         </div>
#       </div>
#     </div>
#   </div>

#   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
#   <script>
#     let isUpdating = false;

#     function updateToGoogleSheet() {
#       if (isUpdating) return;
      
#       isUpdating = true;
#       const button = document.getElementById('updateGoogleSheet');
#       const alertContainer = document.getElementById('alertContainer');
      
#       // Add loading state
#       button.classList.add('btn-loading');
#       button.disabled = true;
      
#       // Clear previous alerts
#       alertContainer.innerHTML = '';
      
#       fetch('/update-google-sheet', {
#         method: 'POST',
#         headers: {
#           'Content-Type': 'application/json',
#         }
#       })
#       .then(response => response.json())
#       .then(data => {
#         // Remove loading state
#         button.classList.remove('btn-loading');
#         button.disabled = false;
#         isUpdating = false;
        
#         if (data.success) {
#           alertContainer.innerHTML = `
#             <div class="alert alert-success">
#               <i class="fas fa-check-circle me-2"></i>
#               <strong>Success!</strong> ${data.message}
#             </div>
#           `;
          
#           // Disable button after successful update
#           button.innerHTML = '<i class="fas fa-check me-2"></i>Data Updated Successfully';
#           button.disabled = true;
#           button.classList.remove('btn-success');
#           button.classList.add('btn-secondary');
#         } else {
#           alertContainer.innerHTML = `
#             <div class="alert alert-warning">
#               <i class="fas fa-exclamation-triangle me-2"></i>
#               <strong>Error:</strong> ${data.message}
#             </div>
#           `;
#         }
#       })
#       .catch(error => {
#         // Remove loading state
#         button.classList.remove('btn-loading');
#         button.disabled = false;
#         isUpdating = false;
        
#         alertContainer.innerHTML = `
#           <div class="alert alert-warning">
#             <i class="fas fa-exclamation-triangle me-2"></i>
#             <strong>Network Error:</strong> Unable to connect to Google Sheets. Please check your internet connection and try again.
#           </div>
#         `;
#       });
#     }
#   </script>
  
# </body>
# </html>
# """

# # ---------------- ROUTES ----------------
# @app.route("/", methods=["GET", "POST"])


# def index():
#     if request.method == "POST":
#         # Store form data in session for later use
#         form_data = {}
#         for field in request.form:
#             form_data[field] = request.form.get(field)
        
#         session['form_data'] = form_data
        
#         # Process PDF generation (same as before)
#         select_outlet = request.form.get("select_outlet")
#         select_type = request.form.get("select_type")
#         Date = request.form.get("Date")
#         No_of_POS_Required = request.form.get("No_of_POS_Required")
#         Merchant_Name_Commercial = request.form.get("Merchant_Name_Commercial")
#         Merchant_Name_Legal = request.form.get("Merchant_Name_Legal")
#         Established_since = request.form.get("Established_since")
#         How_long_at_this_location = request.form.get("How_long_at_this_location")
#         Business_Address_Commercial = request.form.get("Business_Address_Commercial")
#         City = request.form.get("City")
#         Telephone1 = request.form.get("Telephone1")
#         Telephone2 = request.form.get("Telephone2")
#         ContactPerson_Name = request.form.get("ContactPerson_Name")
#         Email_Web = request.form.get("Email_Web")
#         Business_Address_Legal = request.form.get("Business_Address_Legal")
#         City1 = request.form.get("City1")
#         Telephone3 = request.form.get("Telephone3")
#         Telephone4 = request.form.get("Telephone4")
#         ContactPerson_Name1 = request.form.get("ContactPerson_Name1")
#         Email_Web1 = request.form.get("Email_Web1")
#         Number_of_Outlets = request.form.get("Number_of_Outlets")
#         Annual_Sales_Volume = request.form.get("Annual_Sales_Volume")
#         Average_Transaction_size = request.form.get("Average_Transaction_size")
#         Legal_Structure = request.form.get("Legal_Structure")
#         Name = request.form.get("Name")
#         Designation = request.form.get("Designation")
#         CNIC_No = request.form.get("CNIC_No")
#         Residence_Address = request.form.get("Residence_Address")
#         DirectorName1 = request.form.get("DirectorName1")
#         DirectorName2 = request.form.get("DirectorName2")
#         DirectorName3 = request.form.get("DirectorName3")
#         CNIC_No1 = request.form.get("CNIC_No1")
#         CNIC_No2 = request.form.get("CNIC_No2")
#         CNIC_No3 = request.form.get("CNIC_No3")
#         NTN = request.form.get("NTN")
#         PaymentMode = request.form.get("PaymentMode")
#         Bank_Name = request.form.get("Bank_Name")
#         IBAN = request.form.get("IBAN")
#         AccountTitle = request.form.get("AccountTitle")
#         City2 = request.form.get("City2")
#         Debit_Card_FED = request.form.get("Debit_Card_FED")
#         Credit_Card_FED = request.form.get("Credit_Card_FED")
#         intl_Card_FED = request.form.get("intl_Card_FED")
#         previous_Credit_Card_acceptance = request.form.get("previous_Credit_Card_acceptance")
#         If_yes = request.form.get("If_yes")
#         Current_Status = request.form.get("Current_Status")
#         TypeNatureofBusinessCategory = request.form.get("TypeNatureofBusinessCategory")
#         Account_number = request.form.get("Account_number")
#         Branch_name = request.form.get("Branch_name")
#         Branch_code = request.form.get("Branch_code")

#         # Address splitting
#         Business_Address_Commercial_1 = ""
#         Business_Address_Legal_1 = ""
#         if Business_Address_Commercial and len(Business_Address_Commercial) > 62:
#             Business_Address_Commercial_1 = Business_Address_Commercial[62:]
#             Business_Address_Commercial = Business_Address_Commercial[:62]

#         if Business_Address_Legal and len(Business_Address_Legal) > 62:
#             Business_Address_Legal_1 = Business_Address_Legal[62:]
#             Business_Address_Legal = Business_Address_Legal[:62]

#         # Text placements (same as before)
#         texts = [
#             (Date, 480, 465, 0),
#             (No_of_POS_Required, 360, 443, 0),
#             (Merchant_Name_Commercial, 190, 420, 0),
#             (Merchant_Name_Legal, 170, 398, 0),
#             (Established_since, 160, 376, 0),
#             (How_long_at_this_location, 430, 376, 0),
#             (Business_Address_Commercial, 200, 354, 0),
#             (City, 430, 333, 0),
#             (Telephone1, 130, 308, 0),
#             (Telephone2, 380, 308, 0),
#             (ContactPerson_Name, 150, 286, 0),
#             (Email_Web, 370, 286, 0),
#             (Business_Address_Legal, 170, 250, 0),
#             (City1, 430, 228, 0),
#             (Telephone3, 130, 205, 0),
#             (Telephone4, 380, 205, 0),
#             (ContactPerson_Name1, 150, 182, 0),
#             (Email_Web1, 100, 160, 0),
#             (Number_of_Outlets, 200, 136, 0),
#             (Annual_Sales_Volume, 200, 115, 0),
#             (Average_Transaction_size, 250, 94, 0),
#             (TypeNatureofBusinessCategory, 210, 70, 0),
#             (Name, 83, 705, 1),
#             (Designation, 280, 705, 1),
#             (CNIC_No, 440, 705, 1),
#             (Residence_Address, 157, 683, 1),
#             (DirectorName1, 140, 660, 1),
#             (DirectorName2, 140, 640, 1),
#             (DirectorName3, 140, 617, 1),
#             (CNIC_No1, 435, 660, 1),
#             (CNIC_No2, 435, 640, 1),
#             (CNIC_No3, 435, 617, 1),
#             (NTN, 130, 594, 1),
#             (Bank_Name, 110, 548, 1),
#             (IBAN, 122, 520, 1),
#             (AccountTitle, 110, 485, 1),
#             (City2, 405, 485, 1),
#             (Debit_Card_FED, 205, 460, 1),
#             (Credit_Card_FED, 350, 460, 1),
#             (intl_Card_FED, 510, 460, 1),
#         ]

#         # Extra address lines
#         if Business_Address_Commercial_1:
#             texts.append((Business_Address_Commercial_1, 35, 332, 0))

#         if Business_Address_Legal_1:
#             texts.append((Business_Address_Legal_1, 40, 228, 0))

#         # Checkboxes logic (same as before)
#         if select_outlet == "New Outlet":
#             texts.append(("✓", 40, 460, 0))
#         elif select_outlet == "Chain Outlet":
#             texts.append(("✓", 125, 460, 0))

#         if select_type == "POS":
#             texts.append(("✓", 40, 438, 0))
#         elif select_type == "Ecommerce":
#             texts.append(("✓", 137, 438, 0))

#         if Legal_Structure == "Proprietorship":
#             texts.append(("✓", 42, 773, 1))
#         elif Legal_Structure == "Partnership (Registered/Unregistered)":
#             texts.append(("✓", 154, 773, 1))
#         elif Legal_Structure == "Pvt Ltd Co.":
#             texts.append(("✓", 383, 773, 1))
#         elif Legal_Structure == "Public Ltd Clubs":
#             texts.append(("✓", 42, 750, 1))
#         elif Legal_Structure == "Others":
#             texts.append(("✓", 154, 750, 1))

#         if PaymentMode == "Direct Credit":
#             texts.append(("✓", 158, 570, 1))
#         elif PaymentMode == "Cheque":
#             texts.append(("✓", 296, 570, 1))
#         elif PaymentMode == "IBFT":
#             texts.append(("✓", 390, 570, 1))

#         if previous_Credit_Card_acceptance == "Yes":
#             texts.append(("✓", 300, 430, 1))
#         elif previous_Credit_Card_acceptance == "No":
#             texts.append(("✓", 350, 430, 1))

#         if If_yes == "MCB":
#             texts.append(("✓", 157, 405, 1))
#         elif If_yes == "HBL":
#             texts.append(("✓", 225, 405, 1))
#         elif If_yes == "BAFL":
#             texts.append(("✓", 292, 405, 1))
#         elif If_yes == "MBL":
#             texts.append(("✓", 360, 405, 1))
#         elif If_yes == "Keenu":
#             texts.append(("✓", 430, 405, 1))

#         if Current_Status == "Active":
#             texts.append(("✓", 226, 380, 1))
#         elif Current_Status == "Terminated":
#             texts.append(("✓", 293, 380, 1))

#         try:
#             safe_name = re.sub(r'[\\/*?:"<>|]', "_", Merchant_Name_Legal or "merchant")
#             pdf_stream = generate_filled_pdf(texts, safe_name)
#             pdf_path = fr"C:\Users\HP\Desktop\Projects\{safe_name}.pdf"
#             with open(pdf_path, "wb") as f:
#               f.write(pdf_stream.read())
#             session['pdf_generated'] = True
#             session['pdf_filename'] = f"{safe_name}.pdf"
#             session['pdf_error'] = ''
#             return redirect(url_for('success'))
#         except Exception as e:
#             session['pdf_generated'] = False
#             session['pdf_filename'] = ''
#             session['pdf_error'] = str(e)
#         return redirect(url_for('success'))

#     return render_template_string(form_html)

# @app.route("/success")
# def success():
#     form_data = session.get('form_data', {})
    
#     pdf_generated = session.get('pdf_generated', False)
#     pdf_filename = session.get('pdf_filename', '')
#     pdf_error = session.get('pdf_error', '')
#     return render_template_string(success_html,
#       merchant_name=form_data.get('Merchant_Name_Legal', 'N/A'),
#       submission_date=form_data.get('Date', 'N/A'),
#       pos_required=form_data.get('No_of_POS_Required', 'N/A'),
#       pdf_generated=pdf_generated,
#       pdf_filename=pdf_filename,
#       pdf_error=pdf_error
#     )
# @app.route('/download/<filename>')
# def download_pdf(filename):
#   pdf_path = f"C:/Users/HP/Desktop/Projects/{filename}"
#   return send_file(pdf_path, as_attachment=True)

# @app.route("/update-google-sheet", methods=["POST"])
# def update_google_sheet_route():
#     form_data = session.get('form_data', {})
    
#     if not form_data:
#         return {"success": False, "message": "No form data found in session"}
    
#     success, message = update_google_sheet(form_data)
    
#     return {"success": success, "message": message}

# if __name__ == "__main__":
#     # IMPORTANT: Add your Google Sheets URL here
#     GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyN-kwS8MMUohF9-B_J0ANaohOAgWCGfZYJGzvVLLSoh0MipEmsNlQnA0MEcH-tN3nn/exec" 
#     print("=" * 50)
#     print("IMPORTANT: Configure Google Sheets Integration")
#     print("=" * 50)
#     print("1. Create a Google Apps Script web app")
#     print("2. Add your Google Sheets URL to GOOGLE_SHEETS_URL variable")
#     print("3. Make sure your Google Script accepts POST requests")
#     print("=" * 50)
    
#     app.run(debug=True, port=5500)











from flask import Flask, render_template_string, request, send_file, redirect, url_for, session
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import os
import uuid
import time
import re
import requests
import io

app = Flask(__name__)
app.secret_key = 'haseeb_key'  # Change this to a random secret key

# Google Sheets configuration
GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyN-kwS8MMUohF9-B_J0ANaohOAgWCGfZYJGzvVLLSoh0MipEmsNlQnA0MEcH-tN3nn/exec"  # Replace with your Google Apps Script web app URL

# Create temp directory for PDFs
TEMP_PDF_DIR = tempfile.mkdtemp()

def cleanup_old_files():
    """Clean up PDF files older than 1 hour"""
    try:
        current_time = time.time()
        for filename in os.listdir(TEMP_PDF_DIR):
            filepath = os.path.join(TEMP_PDF_DIR, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getctime(filepath)
                # Delete files older than 1 hour (3600 seconds)
                if file_age > 3600:
                    os.remove(filepath)
    except Exception as e:
        print(f"Error cleaning up files: {e}")

# ---------------- SAFE TEXT HELPER ----------------
def safe_text(value):
    return str(value) if value else ""

# ---------------- PDF GENERATION FUNCTION ----------------
# Generate PDF in memory and return it directly
def generate_filled_pdf(texts, safe_name):
    input_pdf_path = "./Form.pdf"
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Group text per page
    page_texts = {}
    for text, x, y, page_number in texts:
        page_texts.setdefault(page_number, []).append((text, x, y))

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]

        if page_num in page_texts:
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=letter)
            for text, x, y in page_texts[page_num]:
                c.drawString(x, y, safe_text(text))
            c.save()

            packet.seek(0)
            new_pdf = PdfReader(packet)
            page.merge_page(new_pdf.pages[0])

        writer.add_page(page)

    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    
    return output_stream

# ---------------- GOOGLE SHEETS FUNCTION ----------------
def update_google_sheet(data):
    """Update Google Sheets with form data"""
    try:
      if not GOOGLE_SHEETS_URL or GOOGLE_SHEETS_URL == "https://docs.google.com/spreadsheets/d/1lXsUaB6PXKbTfkabKTunSlhGEvczxI45gjN4C3kZGCc/edit?usp=sharing":
        return False, "Google Sheets Web App URL not configured. Please deploy your Apps Script as a web app and set the URL."  
      # Prepare data for Google Sheets (as a row)
      sheet_data = [
        data.get('Date', ''),
        data.get('No_of_POS_Required', ''),
        data.get('Merchant_Name_Commercial', ''),
        data.get('Merchant_Name_Legal', ''),
        data.get('Established_since', ''),
        data.get('How_long_at_this_location', ''),
        data.get('Business_Address_Commercial', ''),
        data.get('City', ''),
        data.get('Telephone1', ''),
        data.get('Telephone2', ''),
        data.get('ContactPerson_Name', ''),
        data.get('Email_Web', ''),
        data.get('Business_Address_Legal', ''),
        data.get('City1', ''),
        data.get('Telephone3', ''),
        data.get('Telephone4', ''),
        data.get('ContactPerson_Name1', ''),
        data.get('Email_Web1', ''),
        data.get('Number_of_Outlets', ''),
        data.get('Annual_Sales_Volume', ''),
        data.get('Average_Transaction_size', ''),
        data.get('Legal_Structure', ''),
        data.get('Name', ''),
        data.get('Designation', ''),
        data.get('CNIC_No', ''),
        data.get('Residence_Address', ''),
        data.get('DirectorName1', ''),
        data.get('DirectorName2', ''),
        data.get('DirectorName3', ''),
        data.get('CNIC_No1', ''),
        data.get('CNIC_No2', ''),
        data.get('CNIC_No3', ''),
        data.get('NTN', ''),
        data.get('PaymentMode', ''),
        data.get('Bank_Name', ''),
        data.get('IBAN', ''),
        data.get('AccountTitle', ''),
        data.get('City2', ''),
        data.get('Debit_Card_FED', ''),
        data.get('Credit_Card_FED', ''),
        data.get('intl_Card_FED', ''),
        data.get('previous_Credit_Card_acceptance', ''),
        data.get('If_yes', ''),
        data.get('Current_Status', ''),
        data.get('TypeNatureofBusinessCategory', ''),
        data.get('Account_number', ''),
        data.get('Branch_name', ''),
        data.get('Branch_code', ''),
        data.get('select_outlet', ''),
        data.get('select_type', '')
      ] 
      # Send POST request to Google Apps Script Web App
      response = requests.post(GOOGLE_SHEETS_URL, json=sheet_data, timeout=10)
      print("Google Sheets response:", response.text)  # Debug log
      if response.status_code == 200:
        try:
          resp_json = response.json()
          if resp_json.get("success"):
            return True, resp_json.get("message", "Data successfully updated to Google Sheets")
          else:
            return False, resp_json.get("message", "Google Sheets did not confirm success.")
        except Exception:
          return True, "Data successfully updated to Google Sheets (no JSON response)"
      else:
        return False, f"Failed to update Google Sheets. Status code: {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
      return False, f"Error connecting to Google Sheets: {str(e)}"
    except Exception as e:
      return False, f"Unexpected error: {str(e)}"

# ---------------- HTML FORM TEMPLATE ----------------
form_html = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Merchant Information Form</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <style>
    :root {
      --primary-color: #2563eb;
      --secondary-color: #64748b;
      --success-color: #10b981;
      --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    body { 
      background: var(--background-gradient);
      min-height: 100vh;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main-container {
      padding: 1rem;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .form-card {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      border-radius: 20px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: var(--card-shadow);
      width: 100%;
      max-width: 800px;
      margin: 2rem 0;
    }

    .form-header {
      background: var(--primary-color);
      color: white;
      padding: 2rem;
      border-radius: 20px 20px 0 0;
      text-align: center;
      position: relative;
      overflow: hidden;
    }

    .form-header::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
    }

    .form-header h2 {
      margin: 0;
      font-weight: 700;
      font-size: clamp(1.5rem, 4vw, 2rem);
      position: relative;
      z-index: 1;
    }

    .form-header .subtitle {
      margin-top: 0.5rem;
      opacity: 0.9;
      font-size: clamp(0.9rem, 2.5vw, 1.1rem);
      position: relative;
      z-index: 1;
    }

    .form-body {
      padding: 2rem;
    }

    .section-header {
      color: var(--primary-color);
      font-weight: 600;
      font-size: 1.25rem;
      margin: 2rem 0 1rem 0;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid #e2e8f0;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .section-header:first-child {
      margin-top: 0;
    }

    .form-control, .form-select {
      border: 2px solid #e2e8f0;
      border-radius: 10px;
      padding: 0.75rem 1rem;
      font-size: 1rem;
      transition: all 0.3s ease;
      background-color: #fafafa;
    }

    .form-control:focus, .form-select:focus {
      border-color: var(--primary-color);
      box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.25);
      background-color: white;
    }

    .form-label {
      font-weight: 600;
      color: var(--secondary-color);
      margin-bottom: 0.5rem;
      font-size: 0.95rem;
    }

    .required-field::after {
      content: '*';
      color: #ef4444;
      margin-left: 4px;
    }

    .btn-submit {
      background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%);
      border: none;
      border-radius: 15px;
      padding: 1rem 2rem;
      font-size: 1.1rem;
      font-weight: 600;
      color: white;
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }

    .btn-submit:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
      background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }

    .director-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 1rem;
      margin-bottom: 1rem;
    }

    .director-card .form-control {
      margin-bottom: 0.5rem;
    }

    .director-card:last-child {
      margin-bottom: 0;
    }

    textarea.form-control {
      resize: vertical;
      min-height: 100px;
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
      .main-container {
        padding: 0.5rem;
      }
      
      .form-body {
        padding: 1.5rem;
      }
      
      .form-header {
        padding: 1.5rem;
      }
      
      .section-header {
        font-size: 1.1rem;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.25rem;
      }
      
      .director-card {
        padding: 0.75rem;
      }
    }

    @media (max-width: 576px) {
      .form-body {
        padding: 1rem;
      }
      
      .form-header {
        padding: 1rem;
      }
      
      .btn-submit {
        padding: 0.875rem 1.5rem;
        font-size: 1rem;
      }
    }

    /* Loading Animation */
    .loading-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      z-index: 9999;
      justify-content: center;
      align-items: center;
    }

    .spinner {
      width: 50px;
      height: 50px;
      border: 5px solid rgba(255, 255, 255, 0.3);
      border-top: 5px solid white;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div class="loading-overlay" id="loadingOverlay">
    <div class="spinner"></div>
  </div>

  <div class="main-container">
    <div class="form-card">
      <div class="form-header">
        <h2><i class="fas fa-store me-2"></i>Merchant Information Form</h2>
        <p class="subtitle">Complete merchant registration and POS setup</p>
      </div>
      
      <div class="form-body">
        <form method="POST" id="merchantForm">
          <!-- Basic Info -->
          <div class="section-header">
            <i class="fas fa-info-circle"></i>
            Basic Information
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Date</label>
              <input type="date" class="form-control" name="Date" required>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Number of POS Required</label>
              <input type="number" class="form-control" name="No_of_POS_Required" min="1" max="50" placeholder="e.g., 2">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Merchant Name (Commercial)</label>
              <input type="text" class="form-control" name="Merchant_Name_Commercial" required placeholder="Trading name">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Merchant Name (Legal)</label>
              <input type="text" class="form-control" name="Merchant_Name_Legal" required placeholder="Legal registered name">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Established Since</label>
              <input type="text" class="form-control" name="Established_since" placeholder="e.g., 2018">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">How long at this location?</label>
              <input type="text" class="form-control" name="How_long_at_this_location" placeholder="e.g., 3 years">
            </div>
          </div>

          <!-- Business Address Commercial -->
          <div class="section-header">
            <i class="fas fa-map-marker-alt"></i>
            Business Address (Commercial)
          </div>
          
          <div class="mb-3">
            <label class="form-label required-field">Address</label>
            <textarea class="form-control" name="Business_Address_Commercial" required placeholder="Enter complete commercial address"></textarea>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">City</label>
              <input type="text" class="form-control" name="City" placeholder="e.g., Karachi">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Number of Outlets</label>
              <input type="number" class="form-control" name="Number_of_Outlets" min="1" placeholder="Total outlets">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Telephone 1</label>
              <input type="tel" class="form-control" name="Telephone1" required placeholder="e.g., 021-12345678">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Telephone 2</label>
              <input type="tel" class="form-control" name="Telephone2" placeholder="Alternative number">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Contact Person</label>
              <input type="text" class="form-control" name="ContactPerson_Name" required placeholder="Contact person name">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Email/Website</label>
              <input type="text" class="form-control" name="Email_Web" placeholder="email@domain.com">
            </div>
          </div>

          <!-- Business Address Legal -->
          <div class="section-header">
            <i class="fas fa-balance-scale"></i>
            Business Address (Legal)
          </div>
          
          <div class="mb-3">
            <label class="form-label required-field">Legal Address</label>
            <textarea class="form-control" name="Business_Address_Legal" required placeholder="Enter complete legal address"></textarea>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">City</label>
              <input type="text" class="form-control" name="City1" placeholder="Legal address city">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Annual Sales Volume</label>
              <input type="text" class="form-control" name="Annual_Sales_Volume" required placeholder="e.g., PKR 10,000,000">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Telephone 1</label>
              <input type="tel" class="form-control" name="Telephone3" placeholder="Legal address phone 1">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Telephone 2</label>
              <input type="tel" class="form-control" name="Telephone4" placeholder="Legal address phone 2">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Contact Person</label>
              <input type="text" class="form-control" name="ContactPerson_Name1" placeholder="Legal contact person">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Email/Website</label>
              <input type="text" class="form-control" name="Email_Web1" placeholder="legal@domain.com">
            </div>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Average Transaction Size</label>
            <input type="text" class="form-control" name="Average_Transaction_size" placeholder="e.g., PKR 2,500">
          </div>

          <!-- Owners/Directors -->
          <div class="section-header">
            <i class="fas fa-users"></i>
            Owner / Directors
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Owner Name</label>
              <input type="text" class="form-control" name="Name" required placeholder="Full name">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Designation</label>
              <input type="text" class="form-control" name="Designation" placeholder="e.g., CEO, Owner">
            </div>
          </div>
          
          <div class="mb-3">
            <label class="form-label required-field">CNIC</label>
            <input type="text" class="form-control" name="CNIC_No" required placeholder="12345-6789012-3" pattern="[0-9]{5}-[0-9]{7}-[0-9]{1}">
          </div>
          
          <div class="mb-3">
            <label class="form-label required-field">Residence Address</label>
            <textarea class="form-control" name="Residence_Address" required placeholder="Complete residential address"></textarea>
          </div>
          
          <div class="row">
            <div class="col-lg-4 col-md-6 mb-3">
              <div class="director-card">
                <label class="form-label">Director 1</label>
                <input type="text" class="form-control" name="DirectorName1" placeholder="Director name">
                <input type="text" class="form-control" name="CNIC_No1" placeholder="CNIC: 12345-6789012-3">
              </div>
            </div>
            <div class="col-lg-4 col-md-6 mb-3">
              <div class="director-card">
                <label class="form-label">Director 2</label>
                <input type="text" class="form-control" name="DirectorName2" placeholder="Director name">
                <input type="text" class="form-control" name="CNIC_No2" placeholder="CNIC: 12345-6789012-3">
              </div>
            </div>
            <div class="col-lg-4 col-md-6 mb-3">
              <div class="director-card">
                <label class="form-label">Director 3</label>
                <input type="text" class="form-control" name="DirectorName3" placeholder="Director name">
                <input type="text" class="form-control" name="CNIC_No3" placeholder="CNIC: 12345-6789012-3">
              </div>
            </div>
          </div>

          <!-- Bank Information -->
          <div class="section-header">
            <i class="fas fa-university"></i>
            Bank Information
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Bank Name</label>
              <input type="text" class="form-control" name="Bank_Name" required placeholder="e.g., HBL, MCB, UBL">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Account Title</label>
              <input type="text" class="form-control" name="AccountTitle" required placeholder="Account holder name">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">Account Number</label>
              <input type="text" class="form-control" name="Account_number" required placeholder="Account number">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label required-field">IBAN</label>
              <input type="text" class="form-control" name="IBAN" required placeholder="PK36SCBL0000001123456702" minlength="24"  maxlength="24" style="text-transform: uppercase;">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label" required-field>City</label>
              <input type="text" class="form-control" name="City2" placeholder="Bank branch city" required>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label required-field">Branch Name</label>
              <input type="text" class="form-control" name="Branch_name" required placeholder="Branch name">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label" required-field>Branch Code</label>
              <input type="text" class="form-control" name="Branch_code" placeholder="Branch code" required>
            </div>
          </div>

          <!-- Options & Fees -->
          <div class="section-header">
            <i class="fas fa-cog"></i>
            Options & Fees
          </div>
          
          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label">Debit Card FED (%)</label>
              <input type="number" class="form-control" name="Debit_Card_FED" step="0.01" placeholder="e.g., 1.5">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Credit Card FED (%)</label>
              <input type="number" class="form-control" name="Credit_Card_FED" step="0.01" placeholder="e.g., 2.5">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">International Card FED (%)</label>
              <input type="number" class="form-control" name="intl_Card_FED" step="0.01" placeholder="e.g., 3.5">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">NTN</label>
              <input type="text" class="form-control" name="NTN" placeholder="National Tax Number">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Type / Nature of Business</label>
              <input type="text" class="form-control" name="TypeNatureofBusinessCategory" placeholder="e.g., Restaurant, Retail">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Outlet Type</label>
              <select class="form-select" name="select_outlet">
                <option value="">Select outlet type</option>
                <option value="New Outlet">New Outlet</option>
                <option value="Chain Outlet">Chain Outlet</option>
              </select>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Business Type</label>
              <select class="form-select" name="select_type">
                <option value="">Select business type</option>
                <option value="POS">POS</option>
                <option value="Ecommerce">Ecommerce</option>
              </select>
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Legal Structure</label>
              <select class="form-select" name="Legal_Structure">
                <option value="">Select legal structure</option>
                <option value="Proprietorship">Proprietorship</option>
                <option value="Partnership (Registered/Unregistered)">Partnership</option>
                <option value="Pvt Ltd Co.">Pvt Ltd Co.</option>
                <option value="Public Ltd Clubs">Public Ltd Clubs</option>
                <option value="Others">Others</option>
              </select>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Payment Mode</label>
              <select class="form-select" name="PaymentMode">
                <option value="">Select payment mode</option>
                <option value="Direct Credit">Direct Credit</option>
                <option value="Cheque">Cheque</option>
                <option value="IBFT">IBFT</option>
              </select>
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label">Previous Credit Card Acceptance</label>
              <select class="form-select" name="previous_Credit_Card_acceptance">
                <option value="">Select</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">If Yes (Bank)</label>
              <select class="form-select" name="If_yes">
                <option value="">Select previous bank</option>
                <option value="MCB">MCB</option>
                <option value="HBL">HBL</option>
                <option value="BAFL">BAFL</option>
                <option value="MBL">MBL</option>
                <option value="Keenu">Keenu</option>
              </select>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Current Status</label>
              <select class="form-select" name="Current_Status">
                <option value="">Select status</option>
                <option value="Active">Active</option>
                <option value="Terminated">Terminated</option>
              </select>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="text-center mt-4">
            <button type="submit" class="btn btn-submit">
              <i class="fas fa-file-pdf me-2"></i>Generate & Download PDF
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    // Form validation and submission
    document.getElementById('merchantForm').addEventListener('submit', function(e) {
      const loadingOverlay = document.getElementById('loadingOverlay');
      loadingOverlay.style.display = 'flex';
    });

    // Auto-format CNIC inputs
    document.querySelectorAll('input[name*="CNIC"]').forEach(input => {
      input.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length >= 5) {
          value = value.substring(0, 5) + '-' + value.substring(5);
        }
        if (value.length >= 13) {
          value = value.substring(0, 13) + '-' + value.substring(13, 14);
        }
        e.target.value = value;
      });
    });

    // Set today's date as default
    document.querySelector('input[name="Date"]').value = new Date().toISOString().split('T')[0];
  </script>
</body>
</html>

"""

# ---------------- SUCCESS PAGE TEMPLATE ----------------
success_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Submission Successful</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <style>
    :root {
      --primary-color: #2563eb;
      --success-color: #10b981;
      --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    body { 
      background: var(--background-gradient);
      min-height: 100vh;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main-container {
      padding: 2rem;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .success-card {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      border-radius: 20px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: var(--card-shadow);
      width: 100%;
      max-width: 600px;
      text-align: center;
      overflow: hidden;
    }

    .success-header {
      background: var(--success-color);
      color: white;
      padding: 3rem 2rem;
      position: relative;
    }

    .success-header::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
    }

    .success-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
      position: relative;
      z-index: 1;
      animation: checkmark 0.6s ease-in-out;
    }

    @keyframes checkmark {
      0% { transform: scale(0); }
      50% { transform: scale(1.2); }
      100% { transform: scale(1); }
    }

    .success-title {
      font-size: 2rem;
      font-weight: 700;
      margin: 0;
      position: relative;
      z-index: 1;
    }

    .success-subtitle {
      margin-top: 0.5rem;
      opacity: 0.9;
      font-size: 1.1rem;
      position: relative;
      z-index: 1;
    }

    .success-body {
      padding: 2rem;
    }

    .success-message {
      font-size: 1.1rem;
      color: #374151;
      margin-bottom: 2rem;
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%);
      border: none;
      border-radius: 15px;
      padding: 1rem 2rem;
      font-size: 1.1rem;
      font-weight: 600;
      color: white;
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
      margin: 0.5rem;
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
      background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }

    .btn-success {
      background: linear-gradient(135deg, var(--success-color) 0%, #059669 100%);
      border: none;
      border-radius: 15px;
      padding: 1rem 2rem;
      font-size: 1.1rem;
      font-weight: 600;
      color: white;
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
      margin: 0.5rem;
    }

    .btn-success:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
      background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }

    .alert {
      border-radius: 10px;
      border: none;
      margin-bottom: 2rem;
    }

    .alert-info {
      background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
      color: #0277bd;
    }

    .alert-success {
      background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
      color: #2e7d32;
    }

    .alert-warning {
      background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%);
      color: #f57c00;
    }

    .info-section {
      background: #f8fafc;
      border-radius: 15px;
      padding: 1.5rem;
      margin: 1.5rem 0;
      border: 1px solid #e2e8f0;
    }

    .info-title {
      font-weight: 600;
      color: var(--primary-color);
      margin-bottom: 1rem;
      font-size: 1.1rem;
    }

    .info-item {
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.5rem;
      padding: 0.25rem 0;
    }

    .info-label {
      font-weight: 500;
      color: #6b7280;
    }

    .info-value {
      font-weight: 600;
      color: #374151;
    }

    /* Loading Animation for buttons */
    .btn-loading {
      position: relative;
      color: transparent !important;
    }

    .btn-loading::after {
      content: '';
      position: absolute;
      width: 20px;
      height: 20px;
      top: 50%;
      left: 50%;
      margin-left: -10px;
      margin-top: -10px;
      border: 2px solid rgba(255,255,255,0.3);
      border-top: 2px solid white;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
      .main-container {
        padding: 1rem;
      }
      
      .success-header {
        padding: 2rem 1rem;
      }
      
      .success-body {
        padding: 1.5rem;
      }
      
      .success-icon {
        font-size: 3rem;
      }
      
      .success-title {
        font-size: 1.5rem;
      }
      
      .btn-primary, .btn-success {
        padding: 0.875rem 1.5rem;
        font-size: 1rem;
        display: block;
        width: 100%;
        margin: 0.5rem 0;
      }
    }
  </style>
</head>
<body>
  <div class="main-container">
    <div class="success-card">
      <div class="success-header">
        <div class="success-icon">
          <i class="fas fa-check-circle"></i>
        </div>
        <h1 class="success-title">PDF Downloaded Successfully!</h1>
        <p class="success-subtitle">Your merchant information form has been processed</p>
      </div>
      
      <div class="success-body">
        <div class="success-message">
          <strong>Perfect!</strong> Your merchant registration form has been submitted successfully.
        </div>

        {% if pdf_generated %}
        <div class="alert alert-success">
          <i class="fas fa-file-pdf me-2"></i>
          <strong>PDF Ready:</strong> {{ pdf_filename }} has been generated successfully!
        </div>
        <a href="/download-pdf" class="btn btn-success mb-2" target="_blank">
          <i class="fas fa-download me-2"></i>Download PDF Now
        </a>
        {% endif %}

        <div class="info-section">
          <div class="info-title">
            <i class="fas fa-info-circle me-2"></i>Submission Details
          </div>
          <div class="info-item">
            <span class="info-label">Merchant Name:</span>
            <span class="info-value">{{ merchant_name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Submission Date:</span>
            <span class="info-value">{{ submission_date }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">POS Required:</span>
            <span class="info-value">{{ pos_required }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">PDF Status:</span>
            <span class="info-value">Downloaded to your device</span>
          </div>
        </div>

        <div id="alertContainer"></div>

        <div class="d-flex flex-wrap justify-content-center">
          <a href="/" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Create New Form
          </a>
          <button id="updateGoogleSheet" class="btn btn-success" onclick="updateToGoogleSheet()">
            <i class="fas fa-upload me-2"></i>Update to Google Sheets
          </button>
        </div>

        <div class="alert alert-info mt-3">
          <i class="fas fa-lightbulb me-2"></i>
          <strong>Next Steps:</strong> Your PDF is ready! Click "Update to Google Sheets" to sync your data with the database for record keeping.
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    let isUpdating = false;

    // Auto-download PDF if generated
    {% if pdf_generated %}
    window.addEventListener('load', function() {
      // Auto-download PDF after 2 seconds
      setTimeout(function() {
        window.open('/download-pdf', '_blank');
      }, 2000);
    });
    {% endif %}

    function updateToGoogleSheet() {
      if (isUpdating) return;
      
      isUpdating = true;
      const button = document.getElementById('updateGoogleSheet');
      const alertContainer = document.getElementById('alertContainer');
      
      // Add loading state
      button.classList.add('btn-loading');
      button.disabled = true;
      
      // Clear previous alerts
      alertContainer.innerHTML = '';
      
      fetch('/update-google-sheet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      .then(response => response.json())
      .then(data => {
        // Remove loading state
        button.classList.remove('btn-loading');
        button.disabled = false;
        isUpdating = false;
        
        if (data.success) {
          alertContainer.innerHTML = `
            <div class="alert alert-success">
              <i class="fas fa-check-circle me-2"></i>
              <strong>Success!</strong> ${data.message}
            </div>
          `;
          
          // Disable button after successful update
          button.innerHTML = '<i class="fas fa-check me-2"></i>Data Updated Successfully';
          button.disabled = true;
          button.classList.remove('btn-success');
          button.classList.add('btn-secondary');
        } else {
          alertContainer.innerHTML = `
            <div class="alert alert-warning">
              <i class="fas fa-exclamation-triangle me-2"></i>
              <strong>Error:</strong> ${data.message}
            </div>
          `;
        }
      })
      .catch(error => {
        // Remove loading state
        button.classList.remove('btn-loading');
        button.disabled = false;
        isUpdating = false;
        
        alertContainer.innerHTML = `
          <div class="alert alert-warning">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>Network Error:</strong> Unable to connect to Google Sheets. Please check your internet connection and try again.
          </div>
        `;
      });
    }
  </script>
  
</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Store form data in session for later use
        form_data = {}
        for field in request.form:
            form_data[field] = request.form.get(field)
        
        session['form_data'] = form_data
        
        # Process PDF generation (same as before)
        select_outlet = request.form.get("select_outlet")
        select_type = request.form.get("select_type")
        Date = request.form.get("Date")
        No_of_POS_Required = request.form.get("No_of_POS_Required")
        Merchant_Name_Commercial = request.form.get("Merchant_Name_Commercial")
        Merchant_Name_Legal = request.form.get("Merchant_Name_Legal")
        Established_since = request.form.get("Established_since")
        How_long_at_this_location = request.form.get("How_long_at_this_location")
        Business_Address_Commercial = request.form.get("Business_Address_Commercial")
        City = request.form.get("City")
        Telephone1 = request.form.get("Telephone1")
        Telephone2 = request.form.get("Telephone2")
        ContactPerson_Name = request.form.get("ContactPerson_Name")
        Email_Web = request.form.get("Email_Web")
        Business_Address_Legal = request.form.get("Business_Address_Legal")
        City1 = request.form.get("City1")
        Telephone3 = request.form.get("Telephone3")
        Telephone4 = request.form.get("Telephone4")
        ContactPerson_Name1 = request.form.get("ContactPerson_Name1")
        Email_Web1 = request.form.get("Email_Web1")
        Number_of_Outlets = request.form.get("Number_of_Outlets")
        Annual_Sales_Volume = request.form.get("Annual_Sales_Volume")
        Average_Transaction_size = request.form.get("Average_Transaction_size")
        Legal_Structure = request.form.get("Legal_Structure")
        Name = request.form.get("Name")
        Designation = request.form.get("Designation")
        CNIC_No = request.form.get("CNIC_No")
        Residence_Address = request.form.get("Residence_Address")
        DirectorName1 = request.form.get("DirectorName1")
        DirectorName2 = request.form.get("DirectorName2")
        DirectorName3 = request.form.get("DirectorName3")
        CNIC_No1 = request.form.get("CNIC_No1")
        CNIC_No2 = request.form.get("CNIC_No2")
        CNIC_No3 = request.form.get("CNIC_No3")
        NTN = request.form.get("NTN")
        PaymentMode = request.form.get("PaymentMode")
        Bank_Name = request.form.get("Bank_Name")
        IBAN = request.form.get("IBAN")
        AccountTitle = request.form.get("AccountTitle")
        City2 = request.form.get("City2")
        Debit_Card_FED = request.form.get("Debit_Card_FED")
        Credit_Card_FED = request.form.get("Credit_Card_FED")
        intl_Card_FED = request.form.get("intl_Card_FED")
        previous_Credit_Card_acceptance = request.form.get("previous_Credit_Card_acceptance")
        If_yes = request.form.get("If_yes")
        Current_Status = request.form.get("Current_Status")
        TypeNatureofBusinessCategory = request.form.get("TypeNatureofBusinessCategory")
        Account_number = request.form.get("Account_number")
        Branch_name = request.form.get("Branch_name")
        Branch_code = request.form.get("Branch_code")

        # Address splitting
        Business_Address_Commercial_1 = ""
        Business_Address_Legal_1 = ""
        if Business_Address_Commercial and len(Business_Address_Commercial) > 62:
            Business_Address_Commercial_1 = Business_Address_Commercial[62:]
            Business_Address_Commercial = Business_Address_Commercial[:62]

        if Business_Address_Legal and len(Business_Address_Legal) > 62:
            Business_Address_Legal_1 = Business_Address_Legal[62:]
            Business_Address_Legal = Business_Address_Legal[:62]

        # Text placements (same as before)
        texts = [
            (Date, 480, 465, 0),
            (No_of_POS_Required, 360, 443, 0),
            (Merchant_Name_Commercial, 190, 420, 0),
            (Merchant_Name_Legal, 170, 398, 0),
            (Established_since, 160, 376, 0),
            (How_long_at_this_location, 430, 376, 0),
            (Business_Address_Commercial, 200, 354, 0),
            (City, 430, 333, 0),
            (Telephone1, 130, 308, 0),
            (Telephone2, 380, 308, 0),
            (ContactPerson_Name, 150, 286, 0),
            (Email_Web, 370, 286, 0),
            (Business_Address_Legal, 170, 250, 0),
            (City1, 430, 228, 0),
            (Telephone3, 130, 205, 0),
            (Telephone4, 380, 205, 0),
            (ContactPerson_Name1, 150, 182, 0),
            (Email_Web1, 100, 160, 0),
            (Number_of_Outlets, 200, 136, 0),
            (Annual_Sales_Volume, 200, 115, 0),
            (Average_Transaction_size, 250, 94, 0),
            (TypeNatureofBusinessCategory, 210, 70, 0),
            (Name, 83, 705, 1),
            (Designation, 280, 705, 1),
            (CNIC_No, 440, 705, 1),
            (Residence_Address, 157, 683, 1),
            (DirectorName1, 140, 660, 1),
            (DirectorName2, 140, 640, 1),
            (DirectorName3, 140, 617, 1),
            (CNIC_No1, 435, 660, 1),
            (CNIC_No2, 435, 640, 1),
            (CNIC_No3, 435, 617, 1),
            (NTN, 130, 594, 1),
            (Bank_Name, 110, 548, 1),
            (IBAN, 122, 520, 1),
            (AccountTitle, 110, 485, 1),
            (City2, 405, 485, 1),
            (Debit_Card_FED, 205, 460, 1),
            (Credit_Card_FED, 350, 460, 1),
            (intl_Card_FED, 510, 460, 1),
        ]

        # Extra address lines
        if Business_Address_Commercial_1:
            texts.append((Business_Address_Commercial_1, 35, 332, 0))

        if Business_Address_Legal_1:
            texts.append((Business_Address_Legal_1, 40, 228, 0))

        # Checkboxes logic (same as before)
        if select_outlet == "New Outlet":
            texts.append(("✓", 40, 460, 0))
        elif select_outlet == "Chain Outlet":
            texts.append(("✓", 125, 460, 0))

        if select_type == "POS":
            texts.append(("✓", 40, 438, 0))
        elif select_type == "Ecommerce":
            texts.append(("✓", 137, 438, 0))

        if Legal_Structure == "Proprietorship":
            texts.append(("✓", 42, 773, 1))
        elif Legal_Structure == "Partnership (Registered/Unregistered)":
            texts.append(("✓", 154, 773, 1))
        elif Legal_Structure == "Pvt Ltd Co.":
            texts.append(("✓", 383, 773, 1))
        elif Legal_Structure == "Public Ltd Clubs":
            texts.append(("✓", 42, 750, 1))
        elif Legal_Structure == "Others":
            texts.append(("✓", 154, 750, 1))

        if PaymentMode == "Direct Credit":
            texts.append(("✓", 158, 570, 1))
        elif PaymentMode == "Cheque":
            texts.append(("✓", 296, 570, 1))
        elif PaymentMode == "IBFT":
            texts.append(("✓", 390, 570, 1))

        if previous_Credit_Card_acceptance == "Yes":
            texts.append(("✓", 300, 430, 1))
        elif previous_Credit_Card_acceptance == "No":
            texts.append(("✓", 350, 430, 1))

        if If_yes == "MCB":
            texts.append(("✓", 157, 405, 1))
        elif If_yes == "HBL":
            texts.append(("✓", 225, 405, 1))
        elif If_yes == "BAFL":
            texts.append(("✓", 292, 405, 1))
        elif If_yes == "MBL":
            texts.append(("✓", 360, 405, 1))
        elif If_yes == "Keenu":
            texts.append(("✓", 430, 405, 1))

        if Current_Status == "Active":
            texts.append(("✓", 226, 380, 1))
        elif Current_Status == "Terminated":
            texts.append(("✓", 293, 380, 1))

        try:
            safe_name = re.sub(r'[\\/*?:"<>|]', "_", Merchant_Name_Legal or "merchant")
            pdf_stream = generate_filled_pdf(texts, safe_name)
            
            # Generate unique filename and save to temp directory
            unique_id = str(uuid.uuid4())
            temp_filename = f"{unique_id}_{safe_name}.pdf"
            temp_filepath = os.path.join(TEMP_PDF_DIR, temp_filename)
            
            # Save PDF to temporary file
            with open(temp_filepath, 'wb') as f:
                f.write(pdf_stream.getvalue())
            
            # Store only the filename in session (not the PDF data)
            session['pdf_temp_file'] = temp_filename
            session['pdf_filename'] = f"{safe_name}.pdf"
            session['pdf_generated'] = True
            
            # Clean up old files
            cleanup_old_files()
            
            return redirect(url_for('success'))
            
        except Exception as e:
            session['pdf_error'] = str(e)
            session['pdf_generated'] = False
            return redirect(url_for('success'))

    return render_template_string(form_html)

@app.route("/success")
def success():
    form_data = session.get('form_data', {})
    pdf_generated = session.get('pdf_generated', False)
    pdf_filename = session.get('pdf_filename', '')
    
    return render_template_string(success_html,
      merchant_name=form_data.get('Merchant_Name_Legal', 'N/A'),
      submission_date=form_data.get('Date', 'N/A'),
      pos_required=form_data.get('No_of_POS_Required', 'N/A'),
      pdf_generated=pdf_generated,
      pdf_filename=pdf_filename
    )

@app.route('/download-pdf')
def download_pdf():
    temp_filename = session.get('pdf_temp_file')
    pdf_filename = session.get('pdf_filename', 'merchant.pdf')
    
    if not temp_filename:
        return redirect(url_for('index'))
    
    temp_filepath = os.path.join(TEMP_PDF_DIR, temp_filename)
    
    if not os.path.exists(temp_filepath):
        return redirect(url_for('index'))
    
    return send_file(
        temp_filepath,
        as_attachment=True,
        download_name=pdf_filename,
        mimetype='application/pdf'
    )

@app.route("/update-google-sheet", methods=["POST"])
def update_google_sheet_route():
    form_data = session.get('form_data', {})
    
    if not form_data:
        return {"success": False, "message": "No form data found in session"}
    
    success, message = update_google_sheet(form_data)
    
    return {"success": success, "message": message}

if __name__ == "__main__":
    # IMPORTANT: Add your Google Sheets URL here
    GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyN-kwS8MMUohF9-B_J0ANaohOAgWCGfZYJGzvVLLSoh0MipEmsNlQnA0MEcH-tN3nn/exec" 
    print("=" * 50)
    print("PDF Direct Download Flask App")
    print("=" * 50)
    print("✅ PDF files temporarily stored for download")
    print("✅ Auto-cleanup of old files (1 hour)")
    print("✅ Google Sheets integration available")
    print(f"✅ Temp directory: {TEMP_PDF_DIR}")
    print("=" * 50)
    
    # Clean up old files on startup
    cleanup_old_files()
    
    app.run(debug=True, port=5500)