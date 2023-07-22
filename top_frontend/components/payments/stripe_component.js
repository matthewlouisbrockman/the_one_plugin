import { useUser } from "@auth0/nextjs-auth0/client";

const STRIPE_PUBLICSHABLE_KEY = process.env.NEXT_PUBLIC_STRIPE_PUBLICSHABLE_KEY;

const STRIPE_TABLE_ID = process.env.NEXT_PUBLIC_STRIPE_TABLE_ID;

const StripeComponent = () => {
  const { user } = useUser();

  //stripe doesn't allow |; im replacing | with _ evertwhere but can just handle this for stripe-specifically instead
  const userId = user?.sub.replace("|", "_");

  return (
    <stripe-pricing-table
      pricing-table-id={STRIPE_TABLE_ID}
      publishable-key={STRIPE_PUBLICSHABLE_KEY}
      client-reference-id={userId}
    ></stripe-pricing-table>
  );
};

export default StripeComponent;
