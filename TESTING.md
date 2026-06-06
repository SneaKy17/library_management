# Library Management System — Testing Documentation

**Author**: Nikhil Saklani  
**App**: `library_management`  
**ERPNext Version**: v15  
**Date**: 2024-01-01  

---

## Test Environment

- ERPNext Version: v15
- Site: `library.localhost`
- Browser: Chrome / Firefox
- Tested by: Nikhil Saklani

---

## Section 1: Library Member Tests

---

### Test 1.1: Create New Member

**Objective**: Verify a new library member can be created successfully with all fields and that auto-generated fields populate correctly.

**Prerequisites**:
- ERPNext is running and logged in as Administrator
- Library Management app is installed

**Steps**:
1. Navigate to **Library Management → Library Member → New**
2. Fill in:
   - First Name: `John`
   - Last Name: `Doe`
   - Email: `john.doe@example.com`
   - Phone: `+91-9876543210`
   - Membership Type: `Standard`
   - Membership Start Date: `2024-01-01`
   - Membership End Date: `2024-12-31`
   - Status: `Active`
3. Click **Save**

**Expected Result**:
- Document saves successfully
- `member_id` is auto-generated (e.g., `LIB-MEM-00001`)
- `full_name` is auto-set to `John Doe`
- Member appears in Library Member list view

**Actual Result**:
- ✅ Member saved with ID `LIB-MEM-00001`
- ✅ `full_name` set to `John Doe`
- ✅ Member visible in list view

**Status**: ✅ Pass

**Screenshot**: `01_create_member.png`

---

### Test 1.2: Edit Member Details

**Objective**: Verify that editing an existing member's details saves correctly.

**Prerequisites**:
- Test 1.1 completed (member `LIB-MEM-00001` exists)

**Steps**:
1. Open member `LIB-MEM-00001`
2. Change **Membership Type** from `Standard` to `Premium`
3. Click **Save**
4. Refresh the page

**Expected Result**:
- Membership Type is saved as `Premium`
- Change is tracked in the document's change log

**Actual Result**:
- ✅ Membership Type updated to `Premium`
- ✅ Change log shows the update

**Status**: ✅ Pass

**Screenshot**: `02_edit_member.png`

---

### Test 1.3: Email Uniqueness Validation

**Objective**: Verify that two members cannot share the same email address.

**Prerequisites**:
- Member with email `john.doe@example.com` exists

**Steps**:
1. Navigate to **Library Management → Library Member → New**
2. Fill in First Name: `Jane`, Last Name: `Smith`
3. Enter Email: `john.doe@example.com` (same as existing member)
4. Fill remaining required fields and click **Save**

**Expected Result**:
- Error message is shown: duplicate/unique constraint violation
- Document is NOT saved

**Actual Result**:
- ✅ Error shown: "Email already exists"
- ✅ Document not saved

**Status**: ✅ Pass

**Screenshot**: `03_email_unique_error.png`

---

### Test 1.4: Member Status Change

**Objective**: Verify that a member's status can be changed from Active to Inactive.

**Prerequisites**:
- Member `LIB-MEM-00001` exists with status `Active`

**Steps**:
1. Open member `LIB-MEM-00001`
2. Change **Status** from `Active` to `Inactive`
3. Click **Save**
4. Reload the page

**Expected Result**:
- Status is saved as `Inactive`

**Actual Result**:
- ✅ Status updated to `Inactive`

**Status**: ✅ Pass

**Screenshot**: `04_member_status.png`

---

### Test 1.5: Delete Member

**Objective**: Verify that a member can be deleted.

**Prerequisites**:
- A test member exists (e.g., `LIB-MEM-00099`) with no linked transactions

**Steps**:
1. Open test member `LIB-MEM-00099`
2. Click **Menu (⋮) → Delete**
3. Confirm deletion in the dialog
4. Navigate to the Library Member list

**Expected Result**:
- Member is removed from the list

**Actual Result**:
- ✅ Member deleted successfully
- ✅ No longer visible in list

**Status**: ✅ Pass

**Screenshot**: `05_delete_member.png`

---

## Section 2: Book Tests

---

### Test 2.1: Create New Book

**Objective**: Verify a new book can be created and all auto-fields populate correctly.

**Prerequisites**:
- ERPNext running, Library Management installed

**Steps**:
1. Navigate to **Library Management → Book → New**
2. Fill in:
   - Title: `The Great Gatsby`
   - Author: `F. Scott Fitzgerald`
   - ISBN: `978-0743273565`
   - Publisher: `Scribner`
   - Publication Year: `1925`
   - Category: `Fiction`
   - Total Copies: `3`
3. Click **Save**

**Expected Result**:
- `book_id` auto-generated as `BOOK-00001`
- `available_copies` automatically set to `3`
- Status set to `Available`
- Book appears in list view

**Actual Result**:
- ✅ `book_id` = `BOOK-00001`
- ✅ `available_copies` = `3`
- ✅ `status` = `Available`

**Status**: ✅ Pass

**Screenshot**: `06_create_book.png`

---

### Test 2.2: Available Copies Auto-Set

**Objective**: Verify `available_copies` equals `total_copies` on new book creation.

**Prerequisites**: None

**Steps**:
1. Create a new book with **Total Copies = 5**
2. Save the book

**Expected Result**:
- `available_copies` is automatically set to `5`

**Actual Result**:
- ✅ `available_copies` = `5` after save

**Status**: ✅ Pass

**Screenshot**: `07_available_copies_auto.png`

---

### Test 2.3: Edit Total Copies

**Objective**: Verify editing `total_copies` reflects correctly.

**Prerequisites**:
- Book with `total_copies = 5`, `available_copies = 5`

**Steps**:
1. Open the book
2. Change **Total Copies** from `5` to `3`
3. Save

**Expected Result**:
- `total_copies` = `3`
- `available_copies` is clamped to `3` (cannot exceed total)

**Actual Result**:
- ✅ `total_copies` updated to `3`
- ✅ `available_copies` clamped to `3`

**Status**: ✅ Pass

**Screenshot**: `08_edit_total_copies.png`

---

### Test 2.4: Negative Copies Validation

**Objective**: Verify that negative `total_copies` is rejected.

**Prerequisites**: Any existing book

**Steps**:
1. Open any book
2. Set **Total Copies** to `-1`
3. Click **Save**

**Expected Result**:
- Validation error: "Total Copies cannot be negative"

**Actual Result**:
- ✅ Error shown: "Total Copies cannot be negative."
- ✅ Document not saved

**Status**: ✅ Pass

**Screenshot**: `09_negative_copies_error.png`

---

### Test 2.5: ISBN Uniqueness

**Objective**: Verify two books cannot share the same ISBN.

**Prerequisites**:
- Book with ISBN `978-0743273565` exists

**Steps**:
1. Create a new book
2. Enter ISBN: `978-0743273565`
3. Click **Save**

**Expected Result**:
- Unique constraint error shown

**Actual Result**:
- ✅ Error: "ISBN already exists"
- ✅ Document not saved

**Status**: ✅ Pass

**Screenshot**: `10_isbn_unique.png`

---

## Section 3: Book Transaction Tests

---

### Test 3.1: Create Issue Transaction

**Objective**: Verify a book can be issued to a member.

**Prerequisites**:
- Active member `LIB-MEM-00001`
- Book `BOOK-00001` with `available_copies > 0`

**Steps**:
1. Navigate to **Library Management → Book Transaction → New**
2. Fill in:
   - Member: `LIB-MEM-00001`
   - Book: `BOOK-00001`
   - Transaction Type: `Issue`
   - Transaction Date: today
   - Due Date: `2024-02-01`
3. Click **Save** then **Submit**

**Expected Result**:
- Transaction saved and submitted
- `available_copies` of `BOOK-00001` decremented by 1

**Actual Result**:
- ✅ Transaction `TXN-00001` created
- ✅ `available_copies` decremented

**Status**: ✅ Pass

**Screenshot**: `11_issue_transaction.png`

---

### Test 3.2: Issue Without Due Date

**Objective**: Verify Issue transaction requires a Due Date.

**Prerequisites**:
- Active member and available book

**Steps**:
1. Create a new Book Transaction
2. Set Transaction Type to `Issue`
3. Leave **Due Date** empty
4. Click **Save**

**Expected Result**:
- Validation error: "Due Date is mandatory for Issue transactions"

**Actual Result**:
- ✅ Error shown as expected
- ✅ Document not saved

**Status**: ✅ Pass

**Screenshot**: `12_issue_no_due_date.png`

---

### Test 3.3: Create Return Transaction

**Objective**: Verify a book can be returned.

**Prerequisites**:
- Existing issue transaction for `BOOK-00001` / `LIB-MEM-00001`

**Steps**:
1. Create a new Book Transaction
2. Set Transaction Type to `Return`
3. Set Return Date to today
4. Click **Save** then **Submit**

**Expected Result**:
- Transaction saved with status `Returned`
- `available_copies` of book incremented by 1

**Actual Result**:
- ✅ Transaction saved as `Returned`
- ✅ `available_copies` incremented

**Status**: ✅ Pass

**Screenshot**: `13_return_transaction.png`

---

### Test 3.4: Return Without Return Date

**Objective**: Verify Return transaction requires a Return Date.

**Prerequisites**:
- Active member and book

**Steps**:
1. Create a new Book Transaction
2. Set Transaction Type to `Return`
3. Leave **Return Date** empty
4. Click **Save**

**Expected Result**:
- Validation error: "Return Date is mandatory for Return transactions"

**Actual Result**:
- ✅ Error shown as expected
- ✅ Document not saved

**Status**: ✅ Pass

**Screenshot**: `14_return_no_date.png`

---

### Test 3.5: Invalid Return Date

**Objective**: Verify Return Date cannot be before Transaction Date.

**Prerequisites**: Any member and book

**Steps**:
1. Create a new Book Transaction (Return type)
2. Set Transaction Date to `2024-06-10`
3. Set Return Date to `2024-06-01` (before transaction date)
4. Click **Save**

**Expected Result**:
- Validation error: "Return Date cannot be before the Transaction Date"

**Actual Result**:
- ✅ Error shown as expected
- ✅ Document not saved

**Status**: ✅ Pass

**Screenshot**: `15_invalid_return_date.png`

---

## Section 4: Integration Tests

---

### Test 4.1: Full Checkout and Return Cycle

**Objective**: Verify the complete flow from issuing a book to returning it.

**Prerequisites**:
- Active member `LIB-MEM-00001`
- Book `BOOK-00001` with `available_copies = 3`

**Steps**:
1. Issue `BOOK-00001` to `LIB-MEM-00001` with due date `2024-02-15` → Submit
2. Check `BOOK-00001` → verify `available_copies = 2`
3. Create a Return transaction for `BOOK-00001` / `LIB-MEM-00001` → Submit
4. Check `BOOK-00001` → verify `available_copies = 3`

**Expected Result**:
- Copies correctly tracked throughout the cycle

**Actual Result**:
- ✅ After issue: `available_copies = 2`
- ✅ After return: `available_copies = 3`

**Status**: ✅ Pass

**Screenshot**: `16_integration_cycle.png`

---

### Test 4.2: Inactive Member Cannot Transact

**Objective**: Verify inactive members cannot issue or return books.

**Prerequisites**:
- Member with status `Inactive`
- Any book

**Steps**:
1. Create a Book Transaction with the Inactive member
2. Set Transaction Type to `Issue`
3. Click **Save**

**Expected Result**:
- Validation error: "Only Active members can perform transactions"

**Actual Result**:
- ✅ Error shown as expected
- ✅ Document not saved

**Status**: ✅ Pass

**Screenshot**: `17_inactive_member_error.png`

---

## Summary

| Section | Tests | Passed | Failed |
|---------|-------|--------|--------|
| Library Member | 5 | 5 | 0 |
| Book | 5 | 5 | 0 |
| Book Transaction | 5 | 5 | 0 |
| Integration | 2 | 2 | 0 |
| **Total** | **17** | **17** | **0** |

All test cases passed successfully. ✅
