<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class HomeController extends Controller
{
    public function index()
    {
        //Run python script with shell_exec
        // $output = shell_exec('python '.app_path().'\PyScripts\hello.py');
        // echo $output;



        //Run python script wtih symfony process
        $text = 'The text you are desperate to analyze :)';
        // $process = new Process(['python', '../app/PyScripts/hello.py']);
        $process = new Process(['python3']);
        $process->run();

        // executes after the command finishes
        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        //Get the output of the python script
        $output = $process->getOutput();

        //Convert output to json
        $output = json_decode($output, true);

        dd($output);
        //Get the data from the output
        $data = $output["data"];


        return Inertia::render('Welcome', [
            'canLogin' => Route::has('login'),
            'canRegister' => Route::has('register'),
            'laravelVersion' => '9.5',
            'phpVersion' => PHP_VERSION,
        ]);
    }
}
