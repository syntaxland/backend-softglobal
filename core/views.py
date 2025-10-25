# core/views.py 
from django.shortcuts import render
from django.urls import reverse 

def home(request):
    # Get the URL for the 'schema-swagger-ui'
    swagger_url = reverse('schema-swagger-ui')
    
    # Pass the URL to the template
    context = {
        'swagger_url': swagger_url,
    }
    
    return render(request, 'core/home.html', context)


# # core/views.py
# from django.http import HttpResponse

# def home(request):
#     html_content = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Welcome</title>
#         <style>
#             body {
#                 /* Center the content horizontally and vertically */
#                 display: flex;
#                 justify-content: center; /* Centers horizontally */
#                 align-items: center;    /* Centers vertically */
#                 min-height: 100vh;      /* Ensures the body takes full viewport height */
#                 margin: 0;              /* Remove default body margin */
#                 font-family: sans-serif;
#             }
#             .message {
#                 /* Optional: Style the message itself */
#                 padding: 20px;
#                 border: 1px solid #ccc;
#                 text-align: center;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="message">
#             <h1>Welcome to the Softglobal API!</h1>
#         </div>
#     </body>
#     </html>
#     """
#     return HttpResponse(html_content)