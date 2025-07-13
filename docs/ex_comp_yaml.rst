Code block with the exmaple yaml file

.. code-block:: yaml

   version: "3.9"
   services:
     app:
       image: my-app:latest
       ports:
         - "8080:80"
       environment:
         - ENV=production
     db:
       image: postgres:13
       volumes:
         - db_data:/var/lib/postgresql/data
   volumes:
     db_data:
