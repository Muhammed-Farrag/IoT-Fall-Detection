"""
MongoDB Database Configuration and Models
For NovaCare Fall Detection System
"""
from datetime import datetime
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
from typing import Optional, List, Dict
import os


class MongoDB:
    """MongoDB connection and operations for Fall Detection System."""
    
    def __init__(self, uri: str = None, db_name: str = "novacare_fall_detection"):
        """
        Initialize MongoDB connection.
        
        Args:
            uri: MongoDB connection URI (default: from env or localhost)
            db_name: Database name
        """
        self.uri = uri or os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.db_name = db_name
        self.client = None
        self.db = None
        
    def connect(self) -> bool:
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print(f"✅ Connected to MongoDB: {self.db_name}")
            self._create_indexes()
            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            return False
    
    def _create_indexes(self):
        """Create indexes for better query performance."""
        # Alerts collection indexes
        self.db.alerts.create_index([("timestamp", DESCENDING)])
        self.db.alerts.create_index([("severity", 1)])
        self.db.alerts.create_index([("acknowledged", 1)])
        
        # Stats collection indexes
        self.db.system_stats.create_index([("timestamp", DESCENDING)])
        
        print("   📊 Indexes created")
    
    def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            print("📴 MongoDB disconnected")
    
    # ===================================
    # ALERTS OPERATIONS
    # ===================================
    
    def create_alert(self, alert_data: dict) -> str:
        """
        Create a new alert in the database.
        
        Args:
            alert_data: Dictionary with alert information
            
        Returns:
            Inserted document ID as string
        """
        alert = {
            "timestamp": alert_data.get("timestamp", datetime.utcnow()),
            "alert_type": alert_data.get("alert_type", "FALL"),
            "severity": alert_data.get("severity", "HIGH"),
            "video_path": alert_data.get("video_path"),
            "location": alert_data.get("location", "Camera 1"),
            "description": alert_data.get("description", "Fall detected"),
            "body_angle": alert_data.get("body_angle", 0),
            "velocity": alert_data.get("velocity", 0),
            "posture": alert_data.get("posture", "unknown"),
            "confidence": alert_data.get("confidence", 0),
            "time_down": alert_data.get("time_down", 0),
            "acknowledged": False,
            "acknowledged_at": None,
            "acknowledged_by": None,
            "email_sent": alert_data.get("email_sent", False),
            "created_at": datetime.utcnow()
        }
        
        result = self.db.alerts.insert_one(alert)
        return str(result.inserted_id)
    
    def get_alerts(self, 
                   page: int = 1, 
                   per_page: int = 20,
                   severity: str = None,
                   acknowledged: bool = None) -> Dict:
        """
        Get alerts with pagination and filtering.
        
        Returns:
            Dictionary with alerts list and pagination info
        """
        query = {}
        
        if severity:
            query["severity"] = severity.upper()
        
        if acknowledged is not None:
            query["acknowledged"] = acknowledged
        
        # Get total count
        total = self.db.alerts.count_documents(query)
        
        # Get paginated results
        skip = (page - 1) * per_page
        alerts = list(
            self.db.alerts.find(query)
            .sort("timestamp", DESCENDING)
            .skip(skip)
            .limit(per_page)
        )
        
        # Convert ObjectId to string
        for alert in alerts:
            alert["_id"] = str(alert["_id"])
        
        return {
            "alerts": alerts,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
            "has_next": skip + per_page < total,
            "has_prev": page > 1
        }
    
    def get_alert_by_id(self, alert_id: str) -> Optional[Dict]:
        """Get a single alert by ID."""
        try:
            alert = self.db.alerts.find_one({"_id": ObjectId(alert_id)})
            if alert:
                alert["_id"] = str(alert["_id"])
            return alert
        except:
            return None
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str = "Admin") -> bool:
        """Mark an alert as acknowledged."""
        try:
            result = self.db.alerts.update_one(
                {"_id": ObjectId(alert_id)},
                {
                    "$set": {
                        "acknowledged": True,
                        "acknowledged_at": datetime.utcnow(),
                        "acknowledged_by": acknowledged_by
                    }
                }
            )
            return result.modified_count > 0
        except:
            return False
    
    def get_alert_stats(self) -> Dict:
        """Get alert statistics for dashboard."""
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        total = self.db.alerts.count_documents({})
        unacknowledged = self.db.alerts.count_documents({"acknowledged": False})
        today = self.db.alerts.count_documents({"timestamp": {"$gte": today_start}})
        
        # Count by severity
        high = self.db.alerts.count_documents({"severity": "HIGH"})
        medium = self.db.alerts.count_documents({"severity": "MEDIUM"})
        low = self.db.alerts.count_documents({"severity": "LOW"})
        
        return {
            "total_alerts": total,
            "unacknowledged_alerts": unacknowledged,
            "today_alerts": today,
            "alerts_by_severity": {
                "high": high,
                "medium": medium,
                "low": low
            }
        }
    
    def get_daily_stats(self, days: int = 7) -> List[Dict]:
        """Get daily alert counts for charts."""
        from datetime import timedelta
        
        stats = []
        now = datetime.utcnow()
        
        for i in range(days - 1, -1, -1):
            day = now - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            count = self.db.alerts.count_documents({
                "timestamp": {
                    "$gte": day_start,
                    "$lt": day_end
                }
            })
            
            stats.append({
                "date": day_start.strftime("%a"),
                "count": count
            })
        
        return stats
    
    # ===================================
    # SYSTEM STATS OPERATIONS
    # ===================================
    
    def log_system_stats(self, stats: dict):
        """Log system performance stats."""
        stats_doc = {
            "timestamp": datetime.utcnow(),
            "cpu_usage": stats.get("cpu_usage", 0),
            "memory_usage": stats.get("memory_usage", 0),
            "camera_status": stats.get("camera_status", "unknown"),
            "detection_fps": stats.get("detection_fps", 0),
            "frames_processed": stats.get("frames_processed", 0)
        }
        self.db.system_stats.insert_one(stats_doc)
    
    def get_latest_stats(self) -> Optional[Dict]:
        """Get the most recent system stats."""
        stats = self.db.system_stats.find_one(
            sort=[("timestamp", DESCENDING)]
        )
        if stats:
            stats["_id"] = str(stats["_id"])
        return stats


# Global MongoDB instance
_mongodb: Optional[MongoDB] = None


def get_mongodb() -> MongoDB:
    """Get or create the global MongoDB instance."""
    global _mongodb
    if _mongodb is None:
        _mongodb = MongoDB()
    return _mongodb


def init_mongodb(uri: str = None) -> MongoDB:
    """Initialize MongoDB connection."""
    global _mongodb
    _mongodb = MongoDB(uri)
    _mongodb.connect()
    return _mongodb
