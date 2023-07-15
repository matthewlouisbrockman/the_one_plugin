import Link from "next/link";
import { useUser } from "@auth0/nextjs-auth0/client";

const LoginButton = () => {
  const { user, error, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error)
    return (
      <div>
        Error: {error.message}{" "}
        <Link href="/api/auth/logout">
          <button className="text-white rounded px-3 py-1">Logout</button>
        </Link>
        <Link href="/api/auth/login">
          <button className="bg-white text-black rounded px-3 py-1">
            Login
          </button>
        </Link>
      </div>
    );

  return (
    <div className="flex bg-white-500 ml-auto">
      <div>
        {!user && (
          <Link href="/api/auth/login">
            <button className="bg-white text-black rounded px-3 py-1">
              Login
            </button>
          </Link>
        )}
        {user && (
          <Link href="/api/auth/logout">
            <button className="text-black rounded px-3 py-1">Logout</button>
          </Link>
        )}
      </div>
    </div>
  );
};

export default LoginButton;
