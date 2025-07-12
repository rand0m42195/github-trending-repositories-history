from flask import Flask, request, jsonify
from subscription_manager import SubscriptionManager
import os

app = Flask(__name__)
subscription_manager = SubscriptionManager()

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to GitHub trending updates"""
    try:
        data = request.get_json()
        email = data.get('email')
        categories = data.get('categories', [])
        repositories = data.get('repositories', [])
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Validate email format (simple validation)
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Add subscription
        subscription_manager.add_email_subscription(email, categories, repositories)
        
        return jsonify({
            'success': True,
            'message': f'Successfully subscribed {email}',
            'subscriptions': {
                'categories': categories,
                'repositories': repositories
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe from GitHub trending updates"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Remove subscription
        subscription_manager.remove_email_subscription(email)
        
        return jsonify({
            'success': True,
            'message': f'Successfully unsubscribed {email}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    """Get all current subscriptions (admin only)"""
    try:
        # Simple admin check (in production, use proper authentication)
        admin_key = request.args.get('admin_key')
        if admin_key != os.getenv('ADMIN_KEY', 'admin123'):
            return jsonify({'error': 'Unauthorized'}), 401
        
        return jsonify({
            'success': True,
            'subscriptions': subscription_manager.subscriptions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'total_subscribers': len(subscription_manager.get_all_subscribers())
    })

if __name__ == '__main__':
    # Only run in development
    if os.getenv('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # For production, use a WSGI server
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000) 