import { HomePage } from "@/components/app/homepage";
import { useUser } from "@auth0/nextjs-auth0/client";
import { useEffect } from "react";
const Index = () => {
  const { user } = useUser();

  return <div>{!user && <HomePage />}</div>;
};

export default Index;
