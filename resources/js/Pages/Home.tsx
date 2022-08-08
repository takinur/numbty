import { InertiaLink } from '@inertiajs/inertia-react';
import React from 'react';
import useRoute from '@/Hooks/useRoute';
import useTypedPage from '@/Hooks/useTypedPage';
import { Head } from '@inertiajs/inertia-react';

interface Props {
  canLogin: boolean;
  canRegister: boolean;
  laravelVersion: string;
  phpVersion: string;
}

export default function Welcome({
  canLogin,
  canRegister,
  laravelVersion,
  phpVersion,
}: Props) {
  const route = useRoute();
  const page = useTypedPage();

  return (
    <div className="relative flex items-top justify-center min-h-screen bg-gray-100 dark:bg-gray-900 sm:items-center sm:pt-0">
      <Head title="Welcome" />

      {canLogin ? (
        <div className="hidden fixed top-0 right-0 px-6 py-4 sm:block">
          {page.props.user ? (
            <InertiaLink
              href={route('dashboard')}
              className="text-sm text-gray-700 underline"
            >
              Dashboard
            </InertiaLink>
          ) : (
            <>
              <InertiaLink
                href={route('login')}
                className="text-sm text-gray-700 underline"
              >
                Log in
              </InertiaLink>

              {canRegister ? (
                <InertiaLink
                  href={route('register')}
                  className="ml-4 text-sm text-gray-700 underline"
                >
                  Register
                </InertiaLink>
              ) : null}
            </>
          )}
        </div>
      ) : null}

      <div className="max-w-6xl mx-auto sm:px-6 lg:px-8">
        <div className="flex justify-center mt-4 sm:items-center sm:justify-between">
          <div className="text-center text-sm text-gray-500 sm:text-left">
            <div className="flex items-center">
              <svg
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="-mt-px w-5 h-5 text-gray-400"
              >
                <path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>

              <a
                href="https://laravel.bigcartel.com"
                className="ml-1 underline"
              >
                Shop
              </a>

              <svg
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                className="ml-4 -mt-px w-5 h-5 text-gray-400"
              >
                <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>

              <a
                href="https://github.com/sponsors/taylorotwell"
                className="ml-1 underline"
              >
                Sponsor
              </a>
            </div>
          </div>

          <div className="ml-4 text-center text-sm text-gray-500 sm:text-right sm:ml-0">
            Laravel v{laravelVersion} (PHP v{phpVersion})
          </div>
        </div>
      </div>
    </div>
  );
}
