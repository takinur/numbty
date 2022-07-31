<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\ExecutableFinder;

class PagesController extends Controller
{
    public function index()
    {

        return Inertia::render('Welcome', [
            'canLogin' => Route::has('login'),
            'canRegister' => Route::has('register'),
            'laravelVersion' => '9.5',
            'phpVersion' => PHP_VERSION,
        ]);

        // $finder = new ExecutableFinder();
        // $python = $finder->find('python');
        // if (null === $python ) {
        //     throw new \RuntimeException('Python executable not found.');
        // }
        $process = new Process(['python3', '../app/PyScripts/hello.py']);
        // // $process = new Process(['python3', '../app/PyScripts/ResumeExtractor.py']);
        $process->run();
        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        // //Run python script with shell_exec
        // $output = shell_exec('python '.app_path().'\PyScripts\hello.py');
        // echo $output;

        $output = json_decode($process->getOutput(), true);


        dd($output);
        //Get the data from the output
        $data = $output["data"];



    }
}
