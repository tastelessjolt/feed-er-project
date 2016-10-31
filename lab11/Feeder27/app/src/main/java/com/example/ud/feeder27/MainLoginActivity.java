package com.example.ud.feeder27;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.support.v7.app.AppCompatActivity;



public class MainLoginActivity extends AppCompatActivity implements OnClickListener {

    Button ok, back, exit;
    TextView result;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_login);

        // Login button clicked
        ok = (Button)findViewById(R.id.btn_login);
        ok.setOnClickListener(this);

        result = (TextView)findViewById(R.id.lbl_result);
    }

    public void postLoginData() {
        // Create a new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();

        /* login.php returns true if username and password is equal to saranga */
        HttpPost httppost = new HttpPost("http://localhost:8027");

        try {
            // Add user name and password
            EditText uname = (EditText)findViewById(R.id.txt_username);
            String username = uname.getText().toString();

            EditText pword = (EditText)findViewById(R.id.txt_password);
            String password = pword.getText().toString();

            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
            nameValuePairs.add(new BasicNameValuePair("username", username));
            nameValuePairs.add(new BasicNameValuePair("password", password));
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

            // Execute HTTP Post Request
            //Log.w("SENCIDE", "Execute HTTP Post Request");
            HttpResponse response = httpclient.execute(httppost);

            String str = inputStreamToString(response.getEntity().getContent()).toString();
            Log.w("SENCIDE", str);

            if(str.toString().equalsIgnoreCase("true"))
            {
                Log.w("SENCIDE", "TRUE");
                result.setText("Login successful");
            }else
            {
                Log.w("SENCIDE", "FALSE");
                result.setText(str);
            }

        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
