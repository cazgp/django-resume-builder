# Approach 



## Database changes

A many-to-one relationship was introduced between the existing resume items and the new resume object.

This will allow for existing data created by users to be left intact and accessible when the new feature goes live. To this end, the database migration creates the new resume table and adds a default resume entry for each user, their existing resume items are then linked to this default resume.

The user FK was removed from the resume item table to maintain 3NF.

## Changes to existing screens/functionality

- The default route has been changed to point to the new resume listing view
- The top level navigation item "Resume" has been renamed to reflect that fact it now links to the new listing view
- Back button on edit resume item view goes to the appropriate views showing the list of items
- In the admin system the resume Item view changed to show the linked resumes' names
- Changes to the resume view, item create view and item edit view in views.py were necessary to ensure users could not access or edit other users data. This change was necessary due to the removal of the user FK from the resume item table.

## New functionality

- A permanent redirect has been created from /resume/ to /resume-listing/ for users with bookmarks to old route. This was done as the old route will now error as it requires the id of the resume to view.
- New resume listing screen has been added as per design
- New resume create and rename screen have been added (base view used as with the existing resume_item views)
- Added ability to edit resumes in admin system
- Deleting a resume in deletes child resume items via cascade so orphans aren't left in the DB

