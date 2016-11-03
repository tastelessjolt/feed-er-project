package com.example.ud.feeder27;

/**
 * Created by ud on 3/11/16.
 */

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.CookiePolicy;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    public static final String LOGIN_URL = "http://192.168.100.9:8027/feeder/studentlogin/";

    public static final String KEY_USERNAME="username";
    public static final String KEY_PASSWORD="password";
    public static final String KEY_CSRF="csrfmiddlewaretoken";

    private EditText editTextUsername;
    private EditText editTextPassword;
    private Button buttonLogin;

    private String username;
    private String password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        editTextUsername = (EditText) findViewById(R.id.editTextUsername);
        editTextPassword = (EditText) findViewById(R.id.editTextPassword);

        buttonLogin = (Button) findViewById(R.id.buttonLogin);

        buttonLogin.setOnClickListener(this);
    }


    private void userLogin() {
        final CookieManager manager = new CookieManager(null, CookiePolicy.ACCEPT_ALL);
        username = editTextUsername.getText().toString().trim();
        password = editTextPassword.getText().toString().trim();

        CookieHandler.setDefault(manager);
        RequestQueue queue = Volley.newRequestQueue(this);

        Intent intent = new Intent(this, CaldroidActivity.class);
        startActivity(intent);



        StringRequest getString = new StringRequest(Request.Method.GET,LOGIN_URL, new Response.Listener<String>() {
            public String csrfstring;
            @Override
            public void onResponse(String getResponse) {
                //CookieManager manager =  new CookieManager();
//                CookieHandler .setDefault(manager);
                csrfstring = null;
                try {
                    Log.d("URI 1", manager.getCookieStore().get(new URI(LOGIN_URL)).toString());
                    csrfstring = manager.getCookieStore().get(new URI(LOGIN_URL)).get(0).toString();
                    csrfstring = csrfstring.split("=")[1];
                    Log.d("CSRF", csrfstring);
                    login(csrfstring);
                } catch(URISyntaxException e){
                    e.printStackTrace();
                }
                Log.d("URIs", manager.getCookieStore().getURIs().toString());
                Log.d("COOKIE", manager.getCookieStore().getCookies().toString());
            }
        },
        new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(MainActivity.this,error.toString(),Toast.LENGTH_LONG ).show();
            }
        });

        queue.add(getString);





//        RequestQueue requestQueue = Volley.newRequestQueue(this);
//        requestQueue.add(stringRequest);
    }

    private void login(final String csrftoken) {
        StringRequest stringRequest = new StringRequest(Request.Method.POST, LOGIN_URL,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("Response", response);
                        if(response.trim().equals("success")){
                            //openProfile();
                        }else{
                            Toast.makeText(MainActivity.this,response,Toast.LENGTH_LONG).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(MainActivity.this,error.toString(),Toast.LENGTH_LONG ).show();
                    }
                }){
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String,String> map = new HashMap<String,String>();
                map.put(KEY_USERNAME,username);
                map.put(KEY_PASSWORD,password);
                map.put(KEY_CSRF,csrftoken);
                return map;
            }
        };
        RequestQueue queue = Volley.newRequestQueue(this);
        queue.add(stringRequest);

        StringRequest getString = new StringRequest(Request.Method.GET,"http://192.168.100.9:8027/feeder/index/", new Response.Listener<String>() {
            @Override
            public void onResponse(String getResponse) {
                Log.d("get", getResponse);

            }
        },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(MainActivity.this,error.toString(),Toast.LENGTH_LONG ).show();
                    }
                });
        queue.add(getString);

    }

    private void openProfile(){
        Intent intent = new Intent(this, ActivityUserProfile.class);
        intent.putExtra(KEY_USERNAME, username);
        startActivity(intent);
    }

    @Override
    public void onClick(View v) {
        userLogin();
    }
}
