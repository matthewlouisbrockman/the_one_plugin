import { useState, useEffect } from "react";
import StripeComponent from "@/components/payments/stripe_component";

export const Account = () => {
  const [isShowing, setIsShowing] = useState(false);

  //check if we're on localhost
  useEffect(() => {
    if (typeof window !== "undefined") {
      if (window.location.hostname === "localhost") setIsShowing(true);
    }
  }, []);

  if (!isShowing)
    return (
      <div>
        <div>Account</div>
        <div>not implemented yet</div>
      </div>
    );

  return (
    <div>
      <StripeComponent />
    </div>
  );
};
export default Account;
