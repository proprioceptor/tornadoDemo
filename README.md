Prerequisite

     Python 3.6+
     Postgresql 9+

Steps to run 

   
   * create postgresql database and replace the connection parameters
   * pip install -r requirements.txt
   * python app.py
   
Endpoints to access data

    * Given the teacher_id return the classes of the teacher 
        /teacherclasses/2/
        
    * 2. Given the student id - return the classes that he attends
        /studentclasses/1/