<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;


class PagesController extends Controller
{
    public function index()
    {

        $response = Http::get('http://127.0.0.1:5000');
        $response = Http::get('http://127.0.0.1:5000/items/25');

        $response = Http::get('http://127.0.0.1:5000/items/05', [
            'name' => 'John Doe',
            'email' => 0,
        ]);

        dd($response->json());

        return Inertia::render('Home', [
            'canLogin' => Route::has('login'),
            'canRegister' => Route::has('register'),
            'laravelVersion' => '9.5',
            'phpVersion' => PHP_VERSION,
            'context' => $response->json(),
        ]);


    }
}
