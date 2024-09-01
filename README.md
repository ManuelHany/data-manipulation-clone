# data-manipulation-clone
flask api service that applies data manipulation services on various data types such as tabular, textual and RGB.

used bullsey debian based python image as this project deals with opencv and other big packages that requires dependencies on debian and not in alpine.

copy enb.local to env

admin is not in separate module however some actions are only implemented by admins such as fetching user by id and email and deleting users
i exluded user creation for ease.

logout now in list not database 

whats is done with rgb will be done with rest tabluar and textual

1- test all apis 
2- run flake 8 
3- see if kuberntese doable if not write markdown steps and submit
