import pytest
from bson import ObjectId
from fastapi import status

pytestmark = pytest.mark.asyncio


class TestTeacherReports:
    async def test_get_teacher_report_success(
        self, client, mock_mongodb, sample_teacher_report
    ):
        """Test successful retrieval of a teacher report."""
        # Add _id to the test document
        doc_id = ObjectId()
        test_doc = {**sample_teacher_report, "_id": doc_id}

        # Insert the test document
        result = await mock_mongodb.insert_one(test_doc)
        assert result.inserted_id == doc_id, "Document was not inserted with correct ID"

        # Verify document was inserted
        inserted_doc = await mock_mongodb.find_one({"_id": doc_id})
        assert inserted_doc is not None, "Document was not inserted into mock database"
        assert inserted_doc["_id"] == doc_id
        assert inserted_doc["teacher"] == sample_teacher_report["teacher"]

        # Test the endpoint
        response = client.get(f"/report/teacher-report/{str(doc_id)}")
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["teacher"] == sample_teacher_report["teacher"]
        assert data["subject"] == sample_teacher_report["subject"]
        assert data["hours_lectures"] == sample_teacher_report["hours_lectures"]
        assert data["hours_exercises"] == sample_teacher_report["hours_exercises"]

    async def test_get_teacher_report_not_found(self, client):
        """Test 404 response when teacher report is not found."""
        non_existent_id = str(ObjectId())
        response = client.get(f"/report/teacher-report/{non_existent_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_teacher_report_success(
        self, client, mock_mongodb, sample_teacher_report
    ):
        """Test successful deletion of a teacher report."""
        # Add _id to the test document
        doc_id = ObjectId()
        test_doc = {**sample_teacher_report, "_id": doc_id}

        # Insert the test document
        result = await mock_mongodb.insert_one(test_doc)
        assert result.inserted_id == doc_id, "Document was not inserted with correct ID"

        # Verify document was inserted
        inserted_doc = await mock_mongodb.find_one({"_id": doc_id})
        assert inserted_doc is not None, "Document was not inserted into mock database"

        # Test the endpoint
        response = client.delete(f"/report/teacher-report/delete/{str(doc_id)}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify the document was deleted
        deleted_doc = await mock_mongodb.find_one({"_id": doc_id})
        assert deleted_doc is None

    async def test_delete_teacher_report_not_found(self, client):
        """Test 404 response when trying to delete non-existent teacher report."""
        non_existent_id = str(ObjectId())
        response = client.delete(f"/report/teacher-report/delete/{non_existent_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
