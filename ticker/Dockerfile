FROM python:3
ADD main.py /
RUN pip install terminaltables
RUN pip install beautifulsoup4
RUN pip install requests
CMD [ "python", "./main.py" ]

#Now you are ready to build an image from this Dockerfile. Run:
#docker build -t python-barcode .

#Run Your Image
#After your image has been built successfully, you can run it as a container. In your terminal, run the command docker images to view your images. You should see an entry for “python-barcode”. Run the new image by entering:

#docker run python-barcode
#You should see what looks like a large ASCII QR code.

