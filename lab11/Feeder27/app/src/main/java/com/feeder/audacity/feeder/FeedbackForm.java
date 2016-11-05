package com.feeder.audacity.feeder;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.FitWindowsViewGroup;
import android.support.v7.widget.LinearLayoutCompat;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.RatingBar;
import android.widget.TextView;

import com.google.gson.Gson;

public class FeedbackForm extends AppCompatActivity {
    View lay;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_feedback_form);
        lay = findViewById(R.id.activity_feedback_form);

        Intent intent = getIntent();
        String questions = intent.getStringExtra(Constants.DEADLINE);

        Gson gson = new Gson();
        Deadline deadline = gson.fromJson(questions,Deadline.class);

        for(Question q : deadline.questions){
            TextView question = new TextView(this);
            question.setText(q.questionText);
            ((LinearLayout) lay).addView(question);
            if (q.questionType.equals("text")) {
                EditText editText = new EditText(this);
                ((LinearLayout) lay).addView(editText);
            }
            else if (q.questionType.equals("rate")){
                RatingBar ratingBar = new RatingBar(this);
                LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(30, 30);
//                ratingBar.setLayoutParams(layoutParams);
                ratingBar.setMax(5);
                ratingBar.setNumStars(5);
                ratingBar.setStepSize(1);
                ((LinearLayout) lay).addView(ratingBar);
            }
        }

    }
}
