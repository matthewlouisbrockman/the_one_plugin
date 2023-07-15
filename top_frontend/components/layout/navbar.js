import LoginButton from "../auth/login_button";

export const NavBar = () => {
  return (
    <div className="h-12 w-full bg-black flex flex-row items-center border-b-2 border-white">
      <div>TheOnePlugin</div>
      <LoginButton />
    </div>
  );
};
