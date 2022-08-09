<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Spatie\Permission\Models\Permission;
use Spatie\Permission\Models\Role;

class PermissionsSeeder extends Seeder
{
  /**
   * Run the database seeds.
   *
   * @return void
   */
  public function run()
  {
    $permissionNames = [
      'view backend',
      'manage users',
      'manage roles',
      'manage permissions',
      'manage settings',
      'manage resumes',
    ];
    $permissions = collect($permissionNames)->map(function ($permission) {
        return ['name' => $permission, 'guard_name' => 'web'];
    });
    Permission::insert($permissions->toArray());

    //Create roles and assign created permissions
    Role::create(['name' => 'super-admin'])->givePermissionTo(Permission::all());
    Role::create(['name' => 'editor'])->givePermissionTo([
      'view backend',
      'manage resumes',
    ]);

    //Assign roles
    User::find(1)->assignRole('super-admin');
    User::find(2)->assignRole('editor');


  }
}
