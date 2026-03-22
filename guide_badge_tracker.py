import pandas as pd
badges_df = pd.read_csv('badges.csv')
badges_df = badges_df[["name","requirements","branch","duplicate","completion","complete","completeRequirements"]]

def menu(): #take user input for what to do
    print("Menu")
    print("-"*50)
    print()

    #only view already started badges?
    complete = input("Would you like to view only started/completed badges? (y/n) ")
    complete = complete.upper()
    while complete != 'Y' and complete != 'N':
        print("Invalid answer.")
        complete = input("Would you like to view only started/completed badges? (y/n) ")
        complete = complete.upper()

    if complete == 'Y':
        started = True
    else:
        started = False

    #add extra filters?
    addFilters = input("Would you like to filter results further? (y/n) ")
    addFilters = addFilters.upper()
    while addFilters != 'Y' and addFilters != 'N':
        print("\nInvalid answer.")
        addFilters = input("Would you like to filter results further? (y/n) ")
        addFilters = addFilters.upper()
    
    print() #to look nice

    if addFilters == 'Y':
        filterList = filters()
        filterList.append(started)
        return filterList
    else:
        return(['N', 'N', 'N', started]) #so that the apply filters call still works

def filters(): #take user input for filters
    print("\nFilters:")
    print("---------------------------------------------------------")
    print()
    print("*Combine filter options by entering multiple letters*\n")

    answer = "" #for filter validation

    while answer != "Y":
        branchFilter = input("Filter by branch? \nG for guides \nB for brownies \nL for ladybirds \nN for no filter \n")
        branchFilter = branchFilter.upper()
        answer = input(f"Is {branchFilter} correct? (y/n) ")
        answer = answer.upper()
    print()
    answer = ""

    while answer != "Y":
        duplicateFilter = input("Filter by duplicates? \nA for all branches \nG for guides \nB for brownies \nL for ladybirds \nNo for no duplicates \nN for no filter \n")
        duplicateFilter = duplicateFilter.upper()
        answer = input(f"Is {duplicateFilter} correct? (y/n) ")
        answer = answer.upper()
    print()
    answer = ""

    print("Important: do not combine completion filters. It will not work.")
    while answer != "Y":
        completeFilter = input("Filter by completion? \nC for complete \nI for incomplete \nN for none \n")
        completeFilter = completeFilter.upper()
        answer = input(f"Is {completeFilter} correct? (y/n) ")
        answer = answer.upper()
    print()
    
    filterList = [branchFilter, duplicateFilter, completeFilter]

    return filterList

def applyFilters(df, filterList): #apply filters to dataframe
    df_filtered = df.copy() #make a copy of the original df to clean

    branchFilter = filterList[0]
    if branchFilter != 'N':
        branchFilter = list(branchFilter)
        nonMatchingBranch = []
        for branch in branchFilter:
            nonMatching = df_filtered.index[df_filtered['branch'] != branch].to_list()
            for item in nonMatching:
                nonMatchingBranch.append(item)

        #make sure not to remove anything that fits at least one of the filters 
        keep = []
        for i in range(len(nonMatchingBranch)): #badge to be checked
            repCount = 0
            for j in range(len(nonMatchingBranch)):
                if i != j:
                    if nonMatchingBranch[i] == nonMatchingBranch[j]:
                        #if the same badge is in the list twice
                        repCount += 1
                    elif repCount != len(branchFilter) and nonMatchingBranch[i] not in keep: #if the badge is not repeated
                        keep.append(nonMatchingBranch[i])
        for badge in keep: #remove the badges from the list to be dropped
            nonMatchingBranch.remove(badge)

        df_filtered.drop(nonMatchingBranch, inplace=True)

    duplicateFilter = filterList[1]
    if duplicateFilter != 'N':
        duplicateFilter = list(duplicateFilter)
        nonMatchingDuplicate = []
        print(duplicateFilter)
    
        for branch in duplicateFilter:
            nonMatching = df_filtered.index[df_filtered['duplicate'] != branch].to_list()
            for item in nonMatching:
                nonMatchingDuplicate.append(item)
        
        #make sure not to remove anything that fits at least one of the filters 
        keep = []
        for i in range(len(nonMatchingDuplicate)): #badge to be checked
            repCount = 0
            for j in range(len(nonMatchingDuplicate)):
                if i != j:
                    if nonMatchingDuplicate[i] == nonMatchingDuplicate[j]: #if the badge is repeated
                        repCount += 1
                    elif repCount != len(duplicateFilter) and nonMatchingDuplicate[i] not in keep: #if the badge isn't repeated
                        keep.append(nonMatchingDuplicate[i])
        
        for badge in keep: #remove the badges from the list to be dropped
            nonMatchingDuplicate.remove(badge)
        df_filtered.drop(nonMatchingDuplicate, inplace=True)

    completeFilter = filterList[2]
    if completeFilter != 'N':
        nonMatchingComplete = df_filtered.index[df_filtered['complete'] != completeFilter].to_list()
        df_filtered.drop(nonMatchingComplete, inplace=True)

    return df_filtered

def displayList(df): #list of filtered badges
    badge_names = df["name"].tolist()
    
    print("Filtered badges:")
    for i in range(len(badge_names)):
        print(f"{i+1}. {badge_names[i]}")

def displayBadge(badgeNum, df): #look at one badge
    badgeNum -= 1
    name = df["name"].iloc[badgeNum]

    branch = df["branch"].iloc[badgeNum]
    if branch == "L":
        branch = "Ladybirds"
    elif branch == "B":
        branch = "Brownies"
    else:
        branch = "Guides"

    duplicate = df["duplicate"].iloc[badgeNum]
    duplicates = []
    if "L" in duplicate or "A" in duplicate and branch != "Ladybirds":
        duplicates.append("Ladybirds")
    if "B" in duplicate or "A" in duplicate and branch != "Brownies":
        duplicates.append("Brownies")
    if "G" in duplicate or "A" in duplicate and branch != "Guides":
        duplicates.append("Guides")
    if "No" in duplicate:
        duplicates.append("None")

    requirements = df["requirements"].iloc[badgeNum]
    if '/' in requirements:
        requirementsList = requirements.split('/')
    else:
        requirementsList = [requirements]

    completion = float(df["completion"].iloc[badgeNum])

    completeRequirements = str(df["completeRequirements"].iloc[badgeNum])
    if '/' in completeRequirements:
        completeReqsList = completeRequirements.split('/')
    elif completeRequirements != 'N':
        completeReqsList = [completeRequirements]
    else:
        completeReqsList = []

    #display
    print("-"*50)
    print(name)
    print("~"*10)
    print(f"Branch: {branch}")

    print(f"Duplicates: {duplicates[0]}", end="")
    for i in range(1, len(duplicates)):
        print(f", {duplicates[i]}", end="")
    
    print("\n") #space out details & tracking

    print(f"Requirements:")
    for i in range(len(requirementsList)):
        if 'OR' in requirementsList[i] or 'AND' in requirementsList[i]: #for badges with multiple options
            if 'OR' in requirementsList[i]:
                options = requirementsList[i].split("OR ")
                added = " OR"
            elif 'AND' in requirementsList[i]:
                options = requirementsList[i].split("AND ")
                added = " AND"
            print(f"{i+1}. {options[0]}")
            for j in range(1, len(options)):
                if j+1 == len(options):
                    print(options[j], end="")
                else:
                    print(options[j]+added)
        else:
            print(f"{i+1}. {requirementsList[i]}", end=" ") #regular badges

        if str(i+1) in completeReqsList: #if the requirement is marked complete
            print(u"\u2713")
        else:
            print()

    print(f"Completion: ", end="[")
    for i in range(1, 101):
        if i < 100 and i <= completion:
            print("#", end="")
        elif i == 100 and i == completion:
            print("#] 100%")
        elif i < 100:
            print(" ", end="")
        else:
            print(f" ] {completion}%")
    
    print()

def update(badgeNum, df): #update badge
    badgeNum -= 1

    requirements = df["requirements"].iloc[badgeNum]
    if '/' in requirements:
        requirementsList = requirements.split('/')
    else:
        requirementsList = [requirements]

    numReqs = len(requirementsList)

    completeReqsData = df["completeRequirements"].iloc[badgeNum]
    completeEnteredReqs = []
    
    #update requirements
    validity = False
    while not validity: #make sure entered requirements are actual requirements
        validity = True
        print("Ignore this message unless the question is repeated: Invalid Value") #explain repeated questions
        chosenReq = input("Pick requirements to complete: (numbers seperated by /) ") #enter requirements

        if '/' in chosenReq: #check answer
            completeEnteredReqs = chosenReq.split('/')
            for req in completeEnteredReqs:
                req = int(req)
                if req > numReqs or req <= 0:
                    validity = False
        else:
            completeEnteredReqs = [chosenReq]
            if int(chosenReq) > numReqs or int(chosenReq) <= 0:
                validity = False

    

    if completeReqsData != "N": #if there are already requirements complete
        #put the entered requirements with the existing requirements
        for req in completeEnteredReqs:
            completeReqsData += "/"+req

        df["completeRequirements"].iloc[badgeNum] = completeReqsData #update dataframe
    else:
        #replace 'N' with the entered requirements
        completeReqsData = completeEnteredReqs[0]
        for i in range(1,len(completeEnteredReqs)):
            completeReqsData += "/"+completeEnteredReqs[i]

        df["completeRequirements"].iloc[badgeNum] = completeReqsData #update dataframe

    #updating completion
    if '/' in completeReqsData:
        completeReqsData = completeReqsData.split('/')
    numComplete = len(completeReqsData)
    completion = round((numComplete/numReqs)*100, 2)
    df["completion"].iloc[badgeNum]  = completion

    #update completion status
    if completion == 100.0:
        df.at[badgeNum, "complete"] = "C"

    print("\nBadge Updated.")
    print(f"Complete requirements: {completeReqsData}")
    print(f"Completion: {completion}%")
    print()
    return df


#Main Code#
print("Guide Badge Tracker")
print("-"*50)
while True:
    filterList = menu()
    badges_df_filtered = applyFilters(badges_df, filterList)
    if filterList[3]:
        nonStarted = badges_df_filtered.index[badges_df_filtered['completion'] <= 0].to_list()
        badges_df_filtered.drop(nonStarted, inplace=True)

    numBadges = len(badges_df_filtered["name"].tolist())
    look = True
    while look == True:
        displayList(badges_df_filtered)
        detailed_look = input(f"Select a badge to have a more detailed look (badge no./0 for back to menu): ")
        while not detailed_look.isdigit(): #make sure it's a num.
            print("Invalid answer. Not a number.")
            detailed_look = input("Select a badge to have a more detailed look (badge no./negative for back to menu): ")

        detailed_look = int(detailed_look) #convert from string
        while detailed_look > numBadges: #make sure it's in the list
            print("Invalid answer. Too high.")
            detailed_look = input("Select a badge to have a more detailed look (badge no./negative for back to menu): ")
            if detailed_look.isdigit(): #make sure new ans is a num
                detailed_look = int(detailed_look)
            else:
                detailed_look = numBadges+1
        
        if detailed_look > 0: #if the user has selected a badge, not menu
            displayBadge(detailed_look, badges_df_filtered)
        else:
            break
        
        ans = input("Update progress? (y/n) ")
        ans = ans.upper()
        while ans != "Y" and ans != "N":
            print("Invalid answer.")
            ans = input("Update progress? (y/n) ")
            ans = ans.upper()
        
        if ans == "Y":
            badges_df_filtered = update(detailed_look, badges_df_filtered)

        ans = input("View another badge? (y/n) ")
        ans = ans.upper()
        while ans != "Y" and ans != "N":
            print("Invalid answer.")
            ans = input("View another badge? (y/n) ")
            ans = ans.upper()

        if ans == 'Y':
            print()
            look = True
        else:
            look = False

    #update main badges df
    for i in range(numBadges):
        name = badges_df_filtered["name"].iloc[i]
        updatedRow = badges_df_filtered.loc[(badges_df["name"] == name)]
        badges_df.loc[(badges_df["name"] == name)] = updatedRow
    
    #save to csv
    badges_df.to_csv("badges.csv")

    print("-"*50)
    print()