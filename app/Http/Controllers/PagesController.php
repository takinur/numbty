<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;


class PagesController extends Controller
{
    public function index()
    {

        // $response = Http::post('http://127.0.0.1:5000/api/v1/resume-extract/', [
        //     'name' => 'Takinur',
        //     'resume' => 'assets/test_resumes/T_004.pdf'
        // ]);
        // // $response = Http::get('http://127.0.0.1:5000/');

        // $responseData = $response->json();
        // // dd($responseData['name']);
        // dd($responseData);
        $response = 'Hello World';
        return Inertia::render('Home', [
            'canLogin' => Route::has('login'),
            'canRegister' => Route::has('register'),
            'laravelVersion' => '9.5',
            'phpVersion' => PHP_VERSION,
            'context' => $response,
        ]);


    }
}
