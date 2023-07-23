from models.db import db
from datetime import datetime

class TOPSubscription(db.Model):
    __tablename__ = 'top_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=True)
    subscription_provider = db.Column(db.String(100), nullable=True) # right now just stripe
    customer_id = db.Column(db.String(100), nullable=True) # stripe customer id
    subscription_id = db.Column(db.String(100), nullable=True, unique=True) # stripe subscription id, we'll use this as the sripe identifier
    subscription_status = db.Column(db.String(100), nullable=True) # active, cancelling, canceled, past_due, trialing, unpaid
    subscription_plan = db.Column(db.String(100), nullable=True) # some id from stripe
    product_id = db.Column(db.String(100), nullable=True) # some id from stripe
    createdat = db.Column(db.Integer, nullable=True) # we're gonna store all this in epoch time
    expires_at = db.Column(db.Integer, nullable=True) # same as above
    canceled_at = db.Column(db.Integer, nullable=True) # same as above
    cancel_at_period_end = db.Column(db.Boolean, nullable=True) # whether or not the subscription will cancel at the end of the period

    def __init__(self, **kwargs):
        # So we need to create this object from the webhook data and it might be out of order; for stripe, subscription_id will be a good indicator of whether or not we need to create a new subscription or update an existing one
        self.user_id = kwargs.get('user_id')
        self.subscription_provider = kwargs.get('subscription_provider')
        self.customer_id = kwargs.get('customer_id')
        self.subscription_id = kwargs.get('subscription_id')
        self.subscription_status = kwargs.get('subscription_status')
        self.subscription_plan = kwargs.get('subscription_plan')
        self.createdat = kwargs.get('createdat')
        self.expires_at = kwargs.get('expires_at')
        self.canceled_at = kwargs.get('canceled_at')
        self.cancel_at_period_end = kwargs.get('cancel_at_period_end')
        self.product_id = kwargs.get('product_id')

    def __repr__(self):
        return f"<Subscription {self.subscription_id}>"
    
    def serialize(self):
        return {
            "subscription_id": self.subscription_id,
            "user_id": self.user_id,
            "subscription_provider": self.subscription_provider,
            "customer_id": self.customer_id,
            "subscription_id": self.subscription_id,
            "subscription_status": self.subscription_status,
            "subscription_plan": self.subscription_plan,
            "createdat": self.createdat,
            "expires_at": self.expires_at,
            "canceled_at": self.canceled_at,
            "cancel_at_period_end": self.cancel_at_period_end,
            "product_id": self.product_id
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        # can do partial updates here
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        db.session.add(self)

        db.session.commit()
        print('updated subscription, here is the new subscription: ', self.serialize())
    
    @classmethod
    def find_by_user_id(cls, user_id):
        # check where status is active, cancelling (not having trial), and expired_at > now (epoch)
        return cls.query.filter_by(user_id=user_id).filter(cls.subscription_status.in_(['active', 'cancelling'])).filter(cls.expires_at > datetime.utcnow().timestamp()).all()
    
    @classmethod
    def find_by_subscription_id(cls, subscription_id):
        return cls.query.filter_by(subscription_id=subscription_id).first()
    
    @classmethod
    def find_by_customer_id(cls, customer_id):
        return cls.query.filter_by(customer_id=customer_id).all()
