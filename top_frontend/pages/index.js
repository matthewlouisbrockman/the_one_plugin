import { HomePage } from "@/components/app/homepage";
import { useUser } from "@auth0/nextjs-auth0/client";
import { Management } from "@/components/app/management";
const Index = () => {
  const { user } = useUser();
  return (
    <div>
      {!user && <HomePage />}
      {user && <Management />}
    </div>
  );
};

export default Index;
