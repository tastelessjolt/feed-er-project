package com.feeder.audacity.feeder;

import java.util.Date;

/**
 * Created by harshith on 5/11/16.
 */

public class Deadline {
    protected String deadlineName;
    protected String courseName;
    protected Date deadline;
    protected Date pubDate;
    protected int uid;
    protected boolean isFeedback;
    protected String description;
    protected static final String NAME_PREFIX = "Deadline_:";
    protected static final String COURSE_PREFIX = "Course_";
}