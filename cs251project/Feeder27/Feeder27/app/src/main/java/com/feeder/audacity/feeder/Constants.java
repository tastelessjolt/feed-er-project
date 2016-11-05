package com.feeder.audacity.feeder;

/**
 * Created by sourabh on 3/11/16.
 */

public class Constants {
    public static String DOMAIN="http://10.0.2.2:8027/";
    public static String LOGIN=DOMAIN+"feeder/studentlogin/";
    public static String API=DOMAIN+"feeder/apiendpoint/";
    public static String GET_COURSES="getcourses";
    public static String GET_FEEDBACKS="getfeedbackforms";
    public static String GET_ASSIGNMENTS="getassignemnts";
    public static String GET_QUESTIONS="getquestions";
    public static String DATE = "date";
    public static String ID = "id";
    public static String DEADLINE = "deadline";
    public static String QUESTION = "question";
    public static int LOGINOK = 0;
    public static int NETWORKERR = 1;
    public static int PASSWORDINCORRECT = 2;
    public static int NOTOKAY = 3;
}
