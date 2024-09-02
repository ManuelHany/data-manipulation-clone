# data-manipulation-clone
Flask api service that applies data manipulation services on various data types such as tabular, textual and RGB.

## Run Code
1. Clone the repository 
```commandline
git clone git@github.com:ManuelHany/data-manipulation-clone.git
```
2. Copy `.env.local` to roo directory not inside app.
3. Rename the copied file to .env
4. Run the following command
```commandline
docker compse up
```
5. Open Schematics Documentation.
```commandline
http://127.0.0.1:5000/swagger
```
6. Utilise the postman exported APIs this should help a lot. 

## Project Walk Through
- Project is implemented using `Flask` framework and `Flask-smorest`. 
- It took me a while to be able to migrate all concepts from `django` to `flask`.
- The project mainly provides a full system for data manipulation and storage for users to upload their files and manipulate the data with variaous options.
- Login system and users is applied. 
- JWT authorization is used. 
- At first I used python alpine base image but then shifted towards bullseye (debian) based image that includes more packages needed by complex python packages such as opencv.
- Not all actions are permitted to all kind of users of course please revise swagger documentation.
- Currently for clarification, logout api stores tokens in ram.
- Implementation is available for RGB data manipulation. 
- Tabular and Textual would be with same criteria.
