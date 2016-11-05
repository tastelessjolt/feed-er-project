package com.feeder.audacity.feeder;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import com.google.gson.Gson;

import java.text.SimpleDateFormat;

public class AssignmentActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_assignment);

        Intent intent = getIntent();
        String parse = intent.getStringExtra(Constants.DEADLINE);
        Gson gson = new Gson();
        Deadline d = gson.fromJson(parse,Deadline.class);

        TextView assignmentName, description, deadline, courseName;
        assignmentName = (TextView) findViewById(R.id.assignment_name);
        description = (TextView) findViewById(R.id.description);
        courseName = (TextView) findViewById(R.id.course);
        deadline = (TextView) findViewById(R.id.deadline);

        assignmentName.setText(d.deadlineName);
        description.setText(d.description);
        courseName.setText(d.courseName);
        SimpleDateFormat df = new SimpleDateFormat("dd/MM/yyyy");
        deadline.setText(df.format(d.deadline));
    }
}
