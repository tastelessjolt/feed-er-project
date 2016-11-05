package com.feeder.audacity.feeder;

/**
 * Created by sourabh on 3/11/16.
 */

public class Constants {
    public static String DOMAIN="http://192.168.0.134:8027/";
    public static String LOGIN=DOMAIN+"feeder/studentlogin/";
    public static String API=DOMAIN+"feeder/apiendpoint/";
    public static String GET_COURSES="getcourses";
    public static String GET_FEEDBACKS="getfeedbackforms";
    public static String GET_ASSIGNMENTS="getassignemnts";
    public static int LOGINOK = 0;
    public static int NETWORKERR = 1;
    public static int PASSWORDINCORRECT = 2;
    public static int NOTOKAY = 3;
}
