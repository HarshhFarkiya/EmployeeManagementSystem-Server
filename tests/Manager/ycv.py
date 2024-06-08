def create_admin_user(self):
        admin_data = {
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpassword",
            "role": "admin",
            "department": "admin_department",
            "is_admin": True,
            "manager_id": None
        }
        response = client.post("/users/", json=admin_data)
        if response.status_code not in [200, 201]:
            print(f"Failed to create admin user: {response.status_code} {response.text}")
    

    def test_create_user(self):
        user_data = {
            "username": "testuser" + os.urandom(4).hex(),
            "email": "testuser" + os.urandom(4).hex() + "@example.com",
            "password": "testpassword",
            "role": "employee",
            "department": "test_department",
            "is_admin": False,
            "manager_id": None
        }
        

        response = client.post("/users/", json=user_data)
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        self.assertEqual(response_json["username"], user_data["username"])
        self.assertEqual(response_json["email"], user_data["email"])
        self.assertEqual(response_json["role"], user_data["role"])
        self.assertEqual(response_json["department"], user_data["department"])
        self.assertIn("id", response_json)


@app.post("/users/", response_model=CreateUser, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    try:  
          
        admin_user = db.query(DBUser).filter(DBUser.role == 'admin').first()
        if not admin_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")
          
        db_user = DBUser(
              
              username=user.username,
              email=user.email,
              password=user.password,
              role=user.role,
              department=user.department,
              manager_id=admin_user.id  
              
            )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    
       
    
    except Exception as e:
      logging.error(f"Failed to create user: {e}")
      print(e)
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")