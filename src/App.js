import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  // State for data and UI
  const [keyword, setKeyword] = useState('');
  const [classSearch, setClassSearch] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [courses, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [results, setResults] = useState([]);
  const [resultMessage, setResultMessage] = useState('No results found for empty search. Try a new search.');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const itemsPerPage = 10; // 10 items per page
  
  const dropdownRef = useRef(null);

  // Parse course string to extract subject prefix and course number
  const parseCourseString = (courseStr) => {
    const prefixMatch = courseStr.match(/Prefix: (.*?)\n/);
    const numberMatch = courseStr.match(/Number: (.*?)\n/);
    const titleMatch = courseStr.match(/Title: (.*?)\n/);
    const descriptionMatch = courseStr.match(/Description: (.*?)}/);
    
    return {
      subject_prefix: prefixMatch ? prefixMatch[1] : '',
      course_number: numberMatch ? numberMatch[1] : '',
      title: titleMatch ? titleMatch[1] : '',
      description: descriptionMatch ? descriptionMatch[1] : ''
    };
  };

  // Parse club string to extract details
  const parseClubString = (clubStr) => {
    //const titleMatch = clubStr.match(/Title: (.*?)\n/);

    const parseClubString = clubStr.split('$$$');
    const titleMatch = parseClubString[0];
    const categoryMatch = parseClubString[1];
    const missionMatch = parseClubString[2];
    const presidentMatch = parseClubString[3];
    const emailMatch = parseClubString[4];
    
    /*
    const titleMatch = clubStr.match(/Title:\s*([^\n]+)/);
    const categoryMatch = clubStr.match(/Category:\s*([^\n]+)/);
    const missionMatch = clubStr.match(/Mission Description:\s*([^}]+)/);
    */
   
    console.log(titleMatch)
    return {
      title: titleMatch.slice(4),//titleMatch ? titleMatch[1] : 'Unknown Club',
      category: categoryMatch, //? categoryMatch[1] : 'Uncategorized',
      mission_description: missionMatch, //? missionMatch[1] : 'No description available',
      president_name: presidentMatch, // These might not be in the string format
      email: emailMatch  // These might not be in the string format
    };
  };

  // Fetch courses for dropdown
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('http://localhost:5000/courses');
        if (!response.ok) throw new Error('Failed to fetch courses');
        
        const stringData = await response.json();
        // Parse the course strings into usable objects
        const parsedCourses = stringData.map(courseStr => parseCourseString(courseStr));
        setCourses(parsedCourses);
        setFilteredCourses(parsedCourses);
      } catch (err) {
        setError('Failed to load courses');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCourses();
  }, []);

  // Filter courses based on input
  useEffect(() => {
    if (classSearch && courses.length > 0) {
      const searchTerm = classSearch.toUpperCase();
      const filtered = courses.filter(course => {
        const courseFullName = `${course.subject_prefix} ${course.course_number}`;
        return courseFullName.toUpperCase().includes(searchTerm);
      });
      setFilteredCourses(filtered);
    } else {
      setFilteredCourses(courses);
    }
  }, [classSearch, courses]);

  // Handle click outside dropdown
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [dropdownRef]);

  // Get current page items
  const getCurrentPageItems = () => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return results.slice(startIndex, endIndex);
  };

  // Handle keyword search
  const handleKeywordSearch = async () => {
    if (keyword.trim() === '') {
      setResults([]);
      setResultMessage('No results found for empty search. Try a new search.');
      setTotalPages(0);
      return;
    }

    try {
      setIsLoading(true);
      const response = await fetch(`http://localhost:5000/query?text=${encodeURIComponent(keyword)}`);
      if (!response.ok) throw new Error('Search failed');
      
      const clubData = await response.text();
      const clubString = clubData.slice(1, -6);
      // const result = `,${clubString},`;
      const clubStrings = clubString.split(/@#",/)
      console.log(clubStrings);
      // Parse the club strings and handle both array and single string responses
      let parsedClubs = [];
      if (Array.isArray(clubStrings)) {
        parsedClubs = clubStrings.map(clubStr => parseClubString(clubStr));
        //console.log(parsedClubs);
      } else if (typeof clubStrings === 'string') {
        // If backend returns a single string
        parsedClubs = [parseClubString(clubStrings)];
      }
      
      setResults(parsedClubs);
      setTotalPages(Math.ceil(parsedClubs.length / itemsPerPage));
      setCurrentPage(1); // Reset to first page on new search
      
      setResultMessage(parsedClubs.length > 0 
        ? `Found ${parsedClubs.length} club(s)` 
        : 'No results found. Try a different search.'
      );
    } catch (err) {
      setError('Search failed');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // Search clubs by course
  const searchClubsByCourse = async (course) => {
    // Create a search term from the course title and description
    const searchTerm = `${course.title} ${course.description}`.split(' ').slice(0, 5).join(' ');
    
    try {
      setIsLoading(true);
      const response = await fetch(`http://localhost:5000/query?text=${encodeURIComponent(searchTerm)}`);
      if (!response.ok) throw new Error('Search by course failed');
      
      const clubStrings = await response.json();
      
      // Parse the club strings
      let parsedClubs = [];
      if (Array.isArray(clubStrings)) {
        parsedClubs = clubStrings.map(clubStr => parseClubString(clubStr));
      } else if (typeof clubStrings === 'string') {
        // If backend returns a single string
        parsedClubs = [parseClubString(clubStrings)];
      }
      
      setResults(parsedClubs);
      setTotalPages(Math.ceil(parsedClubs.length / itemsPerPage));
      setCurrentPage(1); // Reset to first page on new search
      
      setResultMessage(parsedClubs.length > 0 
        ? `Found ${parsedClubs.length} club(s) related to ${course.subject_prefix} ${course.course_number}` 
        : `No clubs found related to ${course.subject_prefix} ${course.course_number}`
      );
    } catch (err) {
      setError('Search by course failed');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle course selection
  const handleCourseSelect = (course) => {
    setClassSearch(`${course.subject_prefix} ${course.course_number}`);
    setShowDropdown(false);
    searchClubsByCourse(course);
  };

  // Generate pagination buttons
  const renderPaginationButtons = () => {
    if (totalPages <= 1) return null;

    const buttons = [];
    
    // Previous button
    buttons.push(
      <button 
        key="prev" 
        onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
        disabled={currentPage === 1}
        className="pagination-button"
      >
        &laquo; Prev
      </button>
    );
    
    // Page number buttons (show max 5 pages with ellipsis)
    const renderPageNumbers = () => {
      if (totalPages <= 5) {
        return Array.from({ length: totalPages }, (_, i) => i + 1).map(num => (
          <button 
            key={num} 
            onClick={() => setCurrentPage(num)}
            className={`pagination-button ${currentPage === num ? 'active' : ''}`}
          >
            {num}
          </button>
        ));
      }
      
      let pages = [];
      
      // Always show first page
      pages.push(
        <button 
          key={1} 
          onClick={() => setCurrentPage(1)}
          className={`pagination-button ${currentPage === 1 ? 'active' : ''}`}
        >
          1
        </button>
      );
      
      // Calculate range of visible page numbers
      let startPage = Math.max(2, currentPage - 1);
      let endPage = Math.min(startPage + 2, totalPages - 1);
      
      // Adjust if near the end
      if (endPage === totalPages - 1) {
        startPage = Math.max(2, endPage - 2);
      }
      
      // Show ellipsis before middle pages if needed
      if (startPage > 2) {
        pages.push(<span key="ellipsis1" className="pagination-ellipsis">...</span>);
      }
      
      // Add middle pages
      for (let i = startPage; i <= endPage; i++) {
        pages.push(
          <button 
            key={i} 
            onClick={() => setCurrentPage(i)}
            className={`pagination-button ${currentPage === i ? 'active' : ''}`}
          >
            {i}
          </button>
        );
      }
      
      // Show ellipsis after middle pages if needed
      if (endPage < totalPages - 1) {
        pages.push(<span key="ellipsis2" className="pagination-ellipsis">...</span>);
      }
      
      // Always show last page
      pages.push(
        <button 
          key={totalPages} 
          onClick={() => setCurrentPage(totalPages)}
          className={`pagination-button ${currentPage === totalPages ? 'active' : ''}`}
        >
          {totalPages}
        </button>
      );
      
      return pages;
    };
    
    buttons.push(...renderPageNumbers());
    
    // Next button
    buttons.push(
      <button 
        key="next" 
        onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
        disabled={currentPage === totalPages}
        className="pagination-button"
      >
        Next &raquo;
      </button>
    );
    
    return <div className="pagination">{buttons}</div>;
  };

  return (
    <div className="app">
      <h1>UTD Clubs</h1>

      <div className="search-container">
        <div className="search-input">
          <svg className="search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input 
            type="text" 
            placeholder="ex. Social Cultural Tutoring Developmental" 
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') handleKeywordSearch();
            }}
          />
          <button onClick={handleKeywordSearch} className="search-button">Search</button>
        </div>
        
        <div className="search-input" ref={dropdownRef}>
          <div className="dropdown">
            <input 
              type="text" 
              placeholder="ex. CS 2336" 
              value={classSearch}
              onChange={(e) => setClassSearch(e.target.value)}
              onClick={() => setShowDropdown(true)}
            />
            {showDropdown && filteredCourses.length > 0 && (
              <div className="dropdown-content show">
                {filteredCourses.slice(0, 50).map((course, index) => (
                  <div 
                    key={index} 
                    onClick={() => handleCourseSelect(course)}
                  >
                    {course.subject_prefix} {course.course_number} - {course.title}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <div id="search-results">
        <p className="no-results">{resultMessage}</p>
        {isLoading && <p className="loading">Loading...</p>}
        {error && <p className="error">{error}</p>}
      </div>

      <div className="results-container">
        {getCurrentPageItems().map((club, index) => (
          <div key={index} className="club-card">
            <h3>{club.title}</h3>
            <p className="club-category">{club.category}</p>
            <p className="club-description">{club.mission_description}</p>
            <div className="club-contact">
              <p>President: {club.president_name}</p>
              <p>Contact: {club.email}</p>
            </div>
          </div>
        ))}
      </div>

      {renderPaginationButtons()}
    </div>
  );
}

export default App;