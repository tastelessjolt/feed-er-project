package com.feeder.audacity.feeder;

import android.content.Intent;
import android.provider.Settings;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.FitWindowsViewGroup;
import android.support.v7.widget.LinearLayoutCompat;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.RatingBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;

import org.json.JSONArray;

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
        final Deadline deadline = gson.fromJson(questions,Deadline.class);
        EditText[] editTexts = null;
        RatingBar[] ratingBars = null;
        if(deadline.textq > 0) {
            editTexts = new EditText[deadline.textq];
        }
        if(deadline.rateq > 0){
            ratingBars = new RatingBar[deadline.rateq];
        }
        int countRate = 0, countText = 0;
        if(editTexts != null || ratingBars != null) {
            for (Question q : deadline.questions) {
                TextView question = new TextView(this);
                question.setText(q.questionText);
                ((LinearLayout) lay).addView(question);
                if (q.questionType.equals("text")) {
                    editTexts[countText] = new EditText(this);
                    ((LinearLayout) lay).addView(editTexts[countText]);
                    countText++;
                } else if (q.questionType.equals("rate")) {
                    ratingBars[countRate] = new RatingBar(this);
                    ratingBars[countRate].setMax(5);
                    ratingBars[countRate].setNumStars(5);
                    ratingBars[countRate].setStepSize(1);
                    ((LinearLayout) lay).addView(ratingBars[countRate]);
                    countRate++;
                }
            }
        }
        Button button = new Button(this);
        button.setText("Submit");
        ((LinearLayout) lay).addView(button);
        class ClickListener implements View.OnClickListener {
            RatingBar[] ratingBars;
            EditText[] editTexts;
            FeedbackForm context;


            public ClickListener(EditText[] editTexts, RatingBar[] ratingBars, FeedbackForm context){
                this.ratingBars = ratingBars;
                this.editTexts = editTexts;
                this.context = context;
            }
            @Override
            public void onClick(View view) {
                String postData = "";
                int countRate = 0;
                int countText = 0;
                for(Question q : deadline.questions) {
                    if (q.questionType.equals("text")) {
                        postData = postData + "&" + "q" + q.pk + "=" + editTexts[countText].getText().toString();
                        countText++;
                    } else if (q.questionType.equals("rate")) {
                        postData = postData + "&" + "q" + q.pk + "=" + (int)
                                ratingBars[countRate].getRating();
                        countRate++;
                    }
                }
                System.out.println(postData);
                PostAnswers getData = new PostAnswers("answer" + postData, context);
                getData.execute();
            }
        }
        ClickListener listener = new ClickListener(editTexts, ratingBars, this);
        button.setOnClickListener(listener);

    }

    public void onBackgroundTaskCompleted(String msg, JSONArray jsonArray){
        if(msg != null) {
            if(msg.equals("success")){
                TextView textView = (TextView) findViewById(R.id.status);
                textView.setText("Done");
                Toast.makeText(this,"Response recorded",Toast.LENGTH_LONG).show();
                finish();
            }
        }
        else {
            System.out.println("Yp!");
        }
    }
}
