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
- The project mainly provides a full system for data manipulation and storage for users to upload their files and manipulate the data with variaous options.
- Login system and users is applied. 
- JWT authorization is used. 
- At first I used python alpine base image but then shifted towards bullseye (debian) based image that includes more packages needed by complex python packages such as opencv.
- Not all actions are permitted to all kind of users of course please revise swagger documentation.
- Currently for clarification, logout api stores tokens in ram.
- 



admin is not in separate module however some actions are only implemented by admins such as fetching user by id and email and deleting users
i exluded user creation for ease.

logout now in list not database 

whats is done with rgb will be done with rest tabluar and textual

template for post man
