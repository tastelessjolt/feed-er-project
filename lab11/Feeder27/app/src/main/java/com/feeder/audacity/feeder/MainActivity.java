package com.feeder.audacity.feeder;

import android.os.Build;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import com.roomorama.caldroid.CaldroidFragment;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        CaldroidFragment caldroidFragment = new CaldroidFragment();
        android.support.v4.app.FragmentTransaction t = getSupportFragmentManager().beginTransaction();
        t.replace(R.id.activity_main, caldroidFragment);
        t.commit();

        //Bundle args = new Bundle();
        //Calendar cal = Calendar.getInstance();
        //args.putInt(CaldroidFragment.MONTH, cal.get(Calendar.MONTH) + 1);
        //args.putInt(CaldroidFragment.YEAR, cal.get(Calendar.YEAR));
        //caldroidFragment.setArguments(args);
    }
}
